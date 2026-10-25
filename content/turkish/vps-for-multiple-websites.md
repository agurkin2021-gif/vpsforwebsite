---
title: "Birden fazla web sitesi için VPS"
description: "Birden fazla web sitesi için VPS: toplam yoğun yüke göre kaynak seçin, kullanıcıları ve veritabanlarını ayırın, ortak arıza riskini ve siteleri ne zaman ayıracağınızı belirleyin."
image: "images/home/vps-for-website-hero.webp"
slug: "birden-fazla-web-sitesi-icin-vps"
---

Birden fazla web sitesi için VPS, birkaç site tek kaynak havuzunu, tek yönetim modelini ve tek arıza alanını güvenle paylaşabildiğinde iyi çalışır. Asıl sınır alan adı sayısı değildir. **Sunucudaki tüm sitelerin CPU, RAM, PHP/uygulama süreçleri, veritabanı işlemleri, depolama, arka plan görevleri ve yedeklerinin toplam en yüksek yüküdür**.

Genel satın alma kararı için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[Kısa yanıt](#quick-answer) · [Mimari aracı](#multi-site-vps-architecture-checker) · [Kapasite](#count-workload-not-domains) · [Yalıtım](#isolate-each-site-deliberately) · [Tek IP](#one-ip-can-host-many-websites) · [Ayırma ölçütleri](#when-to-split-sites-or-workloads) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

Bunlar mevcut VDSina Standard paketleri için başlangıç noktalarıdır; sabit site sayısı garantisi değildir.

| Site grubu | Pratik başlangıç noktası | Doğrulanacak noktalar |
|---|---:|---|
| Birkaç hafif statik/önbellekli site | **1 vCPU / 2 GB / 40 GB** | toplam RAM, depolama, yedekler ve ara sıra dinamik işlemler |
| Birkaç mütevazı WordPress/kurumsal site | **2 vCPU / 4 GB / 80 GB** | PHP havuzları, veritabanı belleği, cron çakışması, yedekleme aralıkları |
| Daha ağır karma site grubu veya daha fazla dinamik site | **4 vCPU / 8 GB / 160 GB** | yoğunluk çakışması, veritabanı rekabeti, bir sitenin diğerlerini etkilemesi, depolama artışı |
| Kritik / yoğun yazma yapan / bağımsız ölçeklenen yükler | **Mimariyi ayırın** | arıza yalıtımı, bağımsız ölçeklendirme, uyumsuz yazılım ortamları |

Güncel VDSina Standard fiyatları 13 Ekim 2026 tarihinde yeniden kontrol edildi:

- 1 vCPU / 1 GB / 10 GB / aylık 1 TB veri aktarımı — **$0.07/gün**;
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/gün**;
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/gün**;
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/gün**.

Paketleri “2 GB = X site” veya “8 GB = Y site” diye okumayın. Önbellekli on tanıtım sitesi, yoğun tek bir WooCommerce mağazasından daha hafif olabilir.

Yazılım bileşenlerini birlikte ele alan kaynak hesapları için [web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) rehberini kullanın.

## Çoklu site VPS mimari aracı {#multi-site-vps-architecture-checker}

Tek VPS'in hâlâ uygun bir ortak arıza alanı olup olmadığına karar vermek için kullanın.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="multi-site-architecture-checker">
  <div class="mb-6">
    <label for="ms-count" class="form-label">Kaç etkin site var?</label>
    <select id="ms-count" class="form-input">
      <option value="few">2–5</option>
      <option value="medium">6–15</option>
      <option value="many">16+</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="ms-heavy" class="form-label">Site grubundaki en ağır iş yükü</label>
    <select id="ms-heavy" class="form-input">
      <option value="light">Statik / önbellekli tanıtım / hafif blog</option>
      <option value="wordpress">Dinamik WordPress / kurumsal CMS</option>
      <option value="store">WooCommerce / işlem odaklı site / üyelik</option>
      <option value="app">Özel uygulama / işçi süreçleri ağırlıklı servis</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="ms-clients" class="form-label">Birbiriyle ilgisiz müşterilerin siteleri var mı?</label>
    <select id="ms-clients" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-critical" class="form-label">Kesintisi iş açısından kritik olacak site var mı?</label>
    <select id="ms-critical" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-mixed" class="form-label">Farklı çalışma ortamları veya uyumsuz bakım/güvenlik gereksinimleri var mı?</label>
    <select id="ms-mixed" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-peaks" class="form-label">Trafik yoğunluğu, içe aktarma, yedekleme veya cron görevleri sık çakışıyor mu?</label>
    <select id="ms-peaks" class="form-input"><option value="no">Nadiren</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-panel" class="form-label">Yönetim modeli</label>
    <select id="ms-panel" class="form-input">
      <option value="panel">Hosting kontrol paneli / çok kullanıcılı arayüz</option>
      <option value="manual">Manuel SSH / Nginx veya Apache</option>
      <option value="containers">Konteynerler / uygulama yalıtımı</option>
    </select>
  </div>
  <button class="btn btn-primary" type="submit">Mimariyi değerlendirin</button>
</form>
<p id="multi-site-architecture-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Site grubunuzun gerçek özelliklerini seçin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("multi-site-architecture-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var count = val("ms-count");
    var heavy = val("ms-heavy");
    var clients = val("ms-clients") === "yes";
    var critical = val("ms-critical") === "yes";
    var mixed = val("ms-mixed") === "yes";
    var peaks = val("ms-peaks") === "yes";
    var panel = val("ms-panel");

    var score = 0;
    if (count === "medium") score += 2;
    if (count === "many") score += 4;
    if (heavy === "wordpress") score += 2;
    if (heavy === "store") score += 4;
    if (heavy === "app") score += 4;
    if (clients) score += 2;
    if (mixed) score += 3;
    if (peaks) score += 2;

    var result;

    if (critical) {
      result = "KRİTİK SİTEYİ AYIRIN: işletme bu ortak etki alanını açıkça kabul etmedikçe, iş açısından kritik yük ilgisiz veya düşük öncelikli sitelerle aynı arıza alanını paylaşmamalıdır.";
    } else if (mixed || score >= 9) {
      result = "İŞ YÜKÜNÜ AYIRIN / MİMARİYİ YENİDEN DEĞERLENDİRİN: farklı yazılım ortamları veya yüksek toplam ihtiyaç, yalnızca VPS'i büyütmek yerine baskın siteyi, veritabanını, işçi süreçlerini ya da müşteri gruplarını ayırmayı gerekçelendirir.";
    } else if (clients || score >= 5) {
      result = "TEK VPS + DAHA GÜÇLÜ YALITIM: bir arada barındırma hâlâ çalışabilir; ancak ayrı kullanıcılar, site kök dizinleri, PHP/uygulama süreçleri, veritabanı erişim bilgileri, günlükler ve geri yükleme yolları kullanın. Site bazında etkiyi izleyin.";
    } else {
      result = "TEK VPS / HAFİF SİTE GRUBU: tek VPS makul başlangıç mimarisidir. Site sınırlarını düzenli tutun, kapasite payı bırakın ve alan adı sayısı yerine toplam yoğun yükü izleyin.";
    }

    if (panel === "panel") {
      result += " Panelin ihtiyacınız olan kullanıcı/hesap yalıtım modelini sağladığını doğrulayın.";
    } else if (panel === "manual") {
      result += " Ayrı sistem kullanıcıları, sunucu blokları/sanal konaklar, PHP havuzları veya uygulama servisleri, veritabanı erişim bilgileri ve günlüklerle yalıtımı açıkça kurun.";
    } else {
      result += " Konteynerler süreç ve bağımlılık yalıtımını iyileştirebilir; ancak orkestrasyon, yedekleme ve izleme karmaşıklığı ekler. Varsayılan olarak değil, yazılım ortamı yarar sağladığı için kullanın.";
    }

    document.getElementById("multi-site-architecture-result").textContent = result;
  });
});
</script>

## Alan adlarını değil, iş yükünü sayın {#count-workload-not-domains}

“Tek VPS kaç site barındırır?” sorusunun güvenilir sabit yanıtı yoktur.

Yararlı bir kapasite modeli:

**çoklu site yükü = toplam normal trafik + çakışan dinamik yoğunluklar + veritabanları + cron/işçi süreçleri + yedekler/içe aktarmalar + panel/e-posta/izleme + kapasite payı**

Örnekler:

- statik veya kapsamlı önbelleklenen on site çok az PHP/veritabanı kapasitesi kullanabilir;
- her biri PHP süreçlerine ve veritabanı yüküne sahip üç kurumsal WordPress sitesi çok daha fazla RAM gerektirebilir;
- tek WooCommerce mağazası ödeme veya indirim döneminde tüm sunucuya baskın gelebilir;
- tek görsel içe aktarma, yedekleme veya güvenlik taraması geçici olarak birkaç sakin sitenin toplamından fazla CPU/G/Ç tüketebilir.

Kontrol panelindeki alan adı sayısını değil, en ağır **eşzamanlı** iş yükünü hesaplayın.

## Tek VPS kaç web sitesi barındırabilir? {#how-many-websites-can-one-vps-host}

Site sayısını yalnızca envanter değeri olarak kullanın.

Kapasite şunlara bağlıdır:

- önbellek isabet oranı;
- önbelleksiz istek eşzamanlılığı;
- PHP/uygulama süreç belleği;
- istek süresi;
- veritabanının etkin veri kümesi;
- yazma yoğunluğu;
- zamanlanmış/arka plan görevleri;
- bot trafiği;
- depolama/medya büyümesi;
- yedekleme aralıkları;
- panel/e-posta yükü;
- bıraktığınız kapasite payı.

Baskın kaynak tüketicilerini belirleyemiyorsanız herhangi bir “N site” tahmininin güven düzeyi düşüktür.

WordPress'e özgü davranışlar için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberini kullanın. İşlem yapan mağaza ayrıca ele alınmalıdır; [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) rehberine bakın.

## Tek IP birçok web sitesi barındırabilir {#one-ip-can-host-many-websites}

Olağan modern siteler her alan adı için ayrı genel IP gerektirmez.

Ada dayalı sanal barındırmada:

1. DNS birkaç alan adını aynı VPS IP'sine yönlendirir;
2. tarayıcı istenen ana makine adını gönderir;
3. Nginx/Apache bu adı doğru sunucu bloğu veya sanal konakla eşleştirir;
4. TLS, sunucunun her ana makine adı için uygun sertifikayı sunabilmesi amacıyla SNI kullanır.

Birbiriyle ilgisiz birçok HTTPS sitesi bu sayede tek IP'de 80/443 portlarını paylaşabilir.

Özel ağ politikaları, eski sistem gereksinimleri, e-posta itibarı veya web dışı servisler için ayrı IP hâlâ önemli olabilir; ancak her site için olağan gereksinim değildir.

## Her siteyi bilinçli biçimde yalıtın {#isolate-each-site-deliberately}

Siteleri farklı klasörlere koymak düzen sağlar; güçlü yalıtım sağlamaz.

Birbiriyle ilgisiz veya müşterilere ait sitelerde mümkün olduğunca ayrı sınırlar tercih edin:

| Sınır | Neden önemli? |
|---|---|
| **Sistem/panel kullanıcısı** | ilgisiz siteler arasında dosya ve erişim bilgisi açığa çıkma riskini azaltır |
| **Site kök dizini** | uygulama dosyalarını ve dağıtım yollarını ayrı tutar |
| **PHP-FPM havuzu / uygulama süreci** | her sitenin kendi kullanıcı ve süreç ayarlarıyla çalışmasını sağlar |
| **Veritabanı + veritabanı kullanıcısı** | erişim bilgilerini ve yedekleme/geri yükleme kapsamını sınırlar |
| **Günlükler** | sorun gidermeyi ve olayın kaynağını belirlemeyi kolaylaştırır |
| **Gizli bilgiler/env dosyaları** | bir uygulamanın diğerinin erişim bilgilerini okumasını önler |
| **Yedek kümesi** | tüm site grubunu geri almadan siteye özel geri yüklemeyi destekler |

Yaygın kötü uygulama, tüm PHP sitelerini aynı Unix kullanıcısıyla ve okunabilir yapılandırma dosyalarıyla çalıştırmaktır. Ele geçirilen tek eklenti, diğer sitelerin de ele geçirilmesine dönüşebilir.

FASTPANEL'in kendi güvenlik rehberi, ayrı siteler için ayrı FASTPANEL kullanıcıları önerir. Hosting arayüzü istiyorsanız [kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) seçeneklerini karşılaştırın; panele özgü iş akışı [FASTPANEL ile VPS hosting]({{< relref "fastpanel-vps-hosting.md" >}}) rehberindedir.

## PHP havuzlarını, uygulama servislerini ve veritabanı erişim bilgilerini ayırın {#separate-php-pools-app-services-and-database-credentials}

PHP sitelerinde ayrı PHP-FPM havuzları şunları yalıtmaya yardımcı olabilir:

- Unix kullanıcısı/grubu;
- işçi süreç sınırları;
- PHP yapılandırması;
- günlükler;
- soketler;
- kaynak davranışı.

Node.js, Python ve özel uygulamalar için ayrı uygulama kullanıcıları/servisleri ile yerel portlar/soketler kullanın.

Veritabanlarında:

- ayrı veritabanları kullanın;
- ayrı erişim bilgileri kullanın;
- her uygulamaya yalnızca ihtiyaç duyduğu yetkileri verin;
- tüm sitelere ortak tek root/yönetici veritabanı hesabı vermeyin.

Bu, kusursuz ve katı müşteri yalıtımı oluşturmaz; ancak etkiyi sınırlamayı ve sorun gidermeyi belirgin biçimde iyileştirir.

## Karma iş yükleri farklı bütçeler gerektirir {#mixed-workloads-need-different-budgets}

Karma site grubunu her site aynıymış gibi boyutlandırmayın.

### Statik / önbellekli siteler {#static--cached-sites}

Genellikle uygulama CPU'su ve veritabanı açısından hafiftir.

### WordPress {#wordpress}

PHP süreçleri, veritabanı, önbellek ve cron için bütçe gerektirir.

### WooCommerce / üyelik / işlem odaklı siteler {#woocommerce--membership--transactional-sites}

Daha fazla dinamik PHP/veritabanı payı ve dikkatli arka plan görevi planlaması gerektirir.

### Özel uygulamalar {#custom-apps}

Sürekli süreçler, kuyruklar, konteynerler, farklı çalışma ortamları veya ayrı portlar gerektirebilir.

Çoğu zaman en ağır site, tüm VPS'in mi büyütüleceğini yoksa o sitenin mi ayrılacağını belirler.

## Kendi siteleriniz birbirini kaynak açısından baskılayabilir {#your-own-sites-can-become-noisy-neighbors}

VPS, ilgisiz paylaşımlı hosting müşterilerine olan bağımlılığın bir kısmını azaltır; ancak siteleri birleştirmek **kendi siteleriniz arasında kaynak rekabeti** yaratır.

Tek site şu nedenlerle orantısız kaynak tüketebilir:

- trafik sıçraması;
- kötü eklenti/sorgu;
- bot saldırısı;
- görsel işleme;
- içe/dışa aktarma;
- güvenlik taraması;
- yedek sıkıştırma;
- kontrolsüz cron;
- günlüklerin aşırı büyümesi;
- veritabanı kilidi/G/Ç baskısı.

Kaynak kullanımını yalnızca sunucu boşken değil, bu olaylar sırasında da izleyin.

Yazılımlarınız destekliyorsa site başına işçi süreç sınırları veya konteyner/cgroup sınırları, tek yükün tüm kaynakları tüketme olasılığını azaltabilir. Ancak belgelerinde belirtilmedikçe kontrol panelinin katı CPU/RAM kotaları uyguladığını varsaymayın.

## Toplam yoğunluklar ortalama kullanımdan daha önemlidir {#combined-peaks-matter-more-than-average-usage}

Çoklu site sunucuları, bağımsız yoğunluklar çakıştığında arızalanır.

Örneğin:

- Site A kampanya trafiği alır;
- Site B veritabanı içe aktarması çalıştırır;
- Site C tam yedeklemeye başlar;
- Site D kötü amaçlı yazılım taraması yapar;
- kontrol paneli günlükleri döndürür;
- veritabanı tamponu zaten büyüktür.

Tek başına her site küçük görünebilir. Birlikte CPU, RAM veya G/Ç kapasitesini tüketebilirler.

Bakım ve arka plan işlerini her site için bağımsız değil, tüm site grubunu kapsayacak biçimde planlayın.

## Manuel yönetim, kontrol paneli veya konteynerler? {#manual-control-panel-or-containers}

### Manuel sunucu blokları / sanal konaklar {#manual-server-blocks--virtual-hosts}

Şu durumlarda uygundur:

- sunucuyu yetkin tek yönetici yönetiyorsa;
- site sayısı makulse;
- yazılım ortamları benzerse;
- otomasyon/betikler yapılandırmayı tutarlı tutuyorsa.

Genel kurulum yolu [VPS üzerinde web sitesi yayınlama]({{< relref "how-to-host-a-website-on-vps.md" >}}) rehberinde ele alınır.

### Hosting kontrol paneli {#hosting-control-panel}

Şu durumlarda yararlıdır:

- çok sayıda alan adı/kullanıcı rutin yönetim gerektiriyorsa;
- müşteriye erişim vermek veya yetki devri önemliyse;
- SSL, PHP, veritabanı, yedek ve e-posta için arayüz istiyorsanız.

Panelin **kullanıcı/hesap modeli**, desteklediğini söylediği alan adı sayısından daha önemlidir.

### Konteynerler {#containers}

Şu durumlarda yararlıdır:

- bağımlılık/çalışma ortamı yalıtımı önemliyse;
- uygulamaların yazılım ortamları farklıysa;
- dağıtımlar konteyner temelliyse;
- ekip konteyner işletimini zaten biliyorsa.

Konteynerler kendiliğinden daha basit değildir. İmaj yaşam döngüsü, ağ, kalıcı birimler, yedekleme ve izleme konularında ek sorumluluk getirir.

## Ajans ve müşteri web siteleri {#agency-and-client-websites}

Ajans kullanımı doğal bir çoklu site örneğidir; ancak sitelerin müşterilere ait olması yalıtım gereksinimini artırır.

Şunları tanımlayın:

- alan adı/DNS kimin kontrolünde;
- ayrı panel/sistem hesapları;
- ayrı veritabanı erişim bilgileri;
- devredilen erişim yetkileri;
- müşteri başına yedekleme sorumluluğu;
- geri yüklemenin hangi kapsamda yapılabildiği;
- müşteri ayrıldığında taşıma/dışa aktarma yolu;
- uygulama güncellemelerinden kimin sorumlu olduğu;
- bir müşteri sitesindeki olayın diğerlerini etkileyip etkileyemeyeceği.

Tüm müşteri siteleri aynı Unix kullanıcısını ve arıza alanını paylaşıyorsa müşteriye “yalıtılmış hosting” vaat etmeyin.

**Ajans web siteleri için VPS** konusu da bu rehberde ele alınır. Müşteri sitelerini bir araya getirirken aşağıdaki yalıtım, sorumluluk ve taşıma ölçütlerini birlikte değerlendirin.

Ortak sunucunun işletim sistemi güncellemelerini, güvenliğini, yedek doğrulamasını, izlemesini ve olaylarını ekipte kimse üstlenmiyorsa müşteri sitelerini birleştirmeden önce bunu çözün: [yönetilen ve yönetilmeyen VPS karşılaştırmasına]({{< relref "managed-vs-unmanaged-vps.md" >}}) bakın.

Mevcut site grubunu tek VPS'e taşırken tüm siteleri kopyalayıp bütün DNS kayıtlarını aynı anda değiştirmeyin. Hazırlayın, test edin ve geri dönüş imkânıyla geçiş yapın; taşıma süreci için [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberini kullanın.

## Yedekler ve geri yükleme kapsamı {#backups-and-restore-granularity}

Tek VPS, birkaç sitenin aynı anda arızalanabileceği anlamına gelir.

Yararlı bir yedekleme tasarımı şu soruları yanıtlamanızı sağlamalıdır:

- yalnızca Site A'yı geri yükleyebilir miyim?
- yalnızca onun veritabanını geri yükleyebilir miyim?
- disk/sunucu kaybından sonra tüm VPS'i kurtarabilir miyim?
- sunucu dışında kopya var mı?
- yedekler arasında ne kadar veri kaybedilebilir?
- diğer sitelerin üzerine yazmadan geri yüklemeyi doğrulayabilir miyim?

Tam sunucu imajı felaket kurtarma için yararlıdır. Ancak ele geçirilen tek siteyi kurtarmak diğer tüm siteleri de eski noktaya döndürmeyi gerektiriyorsa tek kurtarma yöntemi olmamalıdır. Saklama süreleri, harici kopyalar, RPO/RTO ve geri yükleme testleri için [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}}) rehberini kullanın.

## Tek VPS, tek arıza alanıdır {#one-vps-is-one-failure-domain}

Birleştirme maliyeti ve tekrarlanan yönetim işini azaltır; fakat arızanın etki alanını büyütür.

Tek olay tüm siteleri etkileyebilir:

- VPS kesintisi;
- dosya sisteminin dolması;
- hatalı işletim sistemi/web yazılımı güncellemesi;
- veritabanı arızası;
- güvenlik duvarı hatası;
- yönetici hesabının ele geçirilmesi;
- kötü amaçlı yazılım/root erişiminin ele geçirilmesi;
- yanlışlıkla silme;
- yedekleme görevinin disk veya G/Ç kapasitesini tüketmesi.

Bu risk vardır. Karar, işletmenin bu riski kabul edip etmediğidir.

## Siteler veya iş yükleri ne zaman ayrılmalı? {#when-to-split-sites-or-workloads}

Gerekçe işletim ölçümleriyle ortaya konabildiğinde ayırın.

Güçlü göstergeler:

- tek site CPU/RAM/G/Ç kaynaklarına sürekli baskın geliyorsa;
- iş açısından kritik site, düşük öncelikli sitelerle kesinti riskini paylaşamıyorsa;
- WooCommerce/mağaza yükü normalde sakin siteleri etkiliyorsa;
- uyumsuz işletim sistemi, çalışma ortamı veya güvenlik gereksinimleri varsa;
- bir veritabanı bağımsız RAM/G/Ç/ölçeklendirme gerektiriyorsa;
- arka plan süreçleri/görevleri kaynaklara baskın geliyorsa;
- bakım aralıkları farklıysa;
- müşteri veya uyumluluk sınırı daha güçlü ayrım gerektiriyorsa;
- optimizasyon ve zamanlama sonrasında kaynak rekabeti sürüyorsa.

Olası ayırma modelleri:

- kritik site -> kendi VPS'i;
- web -> ayrı veritabanı VPS'i;
- web -> ayrı arka plan süreç VPS'i;
- ajanslar -> ayrı müşteri grupları;
- canlı ortam -> ayrı test ortamı;
- yoğun yazma/mağaza yükü -> ayrı sunucu.

Otomatik olarak ayırmayın: her ek VPS izleme, yedekleme, yama, ağ ve olay müdahalesi kapsamını artırır.

## Çoklu site VPS'ini izleme {#monitoring-a-multi-site-vps}

İki düzeyde izleyin.

### Sunucu düzeyi {#server-level}

- CPU;
- RAM/swap/OOM;
- disk kullanımı;
- G/Ç beklemesi;
- veritabanı sağlığı;
- ağ;
- süreç/servis sağlığı.

### Site düzeyi {#site-level}

- önemli her ana makine adı için harici HTTP(S) kontrolü;
- yanıt süresi;
- 5xx hataları;
- PHP/uygulama günlükleri;
- mevcutsa site bazında trafik/süreç baskısı;
- cron/kuyruk hataları;
- veritabanı/günlük/depolama büyümesi.

Bir sanal konak, sertifika veya uygulama bozukken sunucu “çalışıyor” görünebilir. Sunucu ve ana makine adı başına uyarı modelinin tamamı [VPS izleme]({{< relref "vps-monitoring.md" >}}) rehberinde ele alınır.

## Çoklu site yayına alma kontrol listesi {#multi-site-launch-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| Kapasite | alan adı sayısına değil, toplam yoğun yüke göre boyutlandırılmış |
| DNS | her ana makine adı bilinçli biçimde sunucuya yönleniyor |
| HTTPS | her ana makine adı için sertifika ve yenileme yolu çalışıyor |
| Yönlendirme | her alan adı için doğru Nginx sunucu bloğu / Apache sanal konağı |
| Kullanıcılar | ilgisiz/müşteri siteleri mümkün olduğunca ayrı hesaplar kullanıyor |
| Dosyalar | ayrı site kök dizinleri ve izinler |
| PHP/uygulamalar | uygun yerlerde ayrı havuzlar/servisler |
| Veritabanları | ayrı veritabanları/erişim bilgileri; ortak yönetici hesabı yok |
| Günlükler | site bazında günlükler ayırt edilebiliyor |
| Görevler | yedekleme/içe aktarma/cron zarar verici çakışmaları önleyecek biçimde planlanmış |
| Yedekler | sunucu dışında kopya ve site düzeyinde geri yükleme yolu |
| İzleme | sunucu ve önemli siteler ayrı kontrol ediliyor |
| Etki alanı | işletme tek VPS arızasının etkisini kabul ediyor |
| Ayırma ölçütü | siteyi/servisi ayırmak için açık koşul var |

## Güncel çoklu site VPS örnekleri {#current-multi-site-vps-examples}

Bu VDSina Standard paketleri yalnızca ihtiyaca eşleme örnekleridir.

| VPS | Uygun başlangıç kullanımı | Ne zaman yeniden değerlendirmeli? |
|---|---|---|
| 1 vCPU / 2 GB / 40 GB — $0.50/gün | birkaç hafif önbellekli/statik site | dinamik PHP/veritabanı çakışması, panel/e-posta, yedekler |
| 2 vCPU / 4 GB / 80 GB — $0.67/gün | birkaç mütevazı kurumsal/WordPress sitesi | mağaza yükü, çok sayıda etkin görev, veritabanı baskısı |
| 4 vCPU / 8 GB / 160 GB — $1.34/gün | daha ağır karma site grubu / daha fazla eşzamanlı etkinlik | kritik yükler ortak arıza alanını paylaşıyorsa veya tek yük bağımsız ölçeklendirme gerektiriyorsa |

1 GB paket testlerde veya çok hafif sitelerde yararlı olabilir; ancak genel çoklu site canlı ortam önerisi olarak sunulmaz.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Çoklu site için güncel VPS seçeneklerini inceleyin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Güncel VPS fiyatlarını doğrulayın; mimariyi ölçülen iş yüküne ve kabul edilebilir arıza riskine göre seçin.</small></p>

## Sık sorulan sorular {#faq}

### Tek VPS'te kaç web sitesi barındırabilirim? {#how-many-websites-can-i-host-on-one-vps}

Güvenilir sabit sayı yoktur. Kapasite tüm sitelerin toplam en yüksek CPU, RAM, PHP/uygulama süreçleri, veritabanı işlemleri, depolama ve arka plan görevi yüküne bağlıdır.

### Birden fazla site ayrı IP adresleri gerektirir mi? {#do-multiple-websites-need-separate-ip-addresses}

Genellikle hayır. Ada dayalı sanal barındırma ve TLS SNI, birden fazla HTTPS alan adının tek genel IP'yi paylaşmasını sağlar. Özel ağ, e-posta veya eski sistem gereksinimlerinde ayrı IP'ler yine de yararlı olabilir.

### Birkaç WordPress sitesi tek VPS'i paylaşabilir mi? {#can-several-wordpress-sites-share-one-vps}

Evet. Ayrı kullanıcılar ve erişim bilgileri kullanın; sunucuyu toplam PHP, veritabanı ve arka plan yüküne göre boyutlandırın. Birkaç hafif WordPress sitesi iyi sığabilir; tek ağır dinamik site sunucuya baskın gelebilir.

### Her sitenin ayrı PHP-FPM havuzu olmalı mı? {#should-every-site-have-a-separate-php-fpm-pool}

İlgisiz veya müşterilere ait PHP sitelerinde ayrı havuzlar süreç/kullanıcı yalıtımını iyileştirip site bazında ayar ve günlük kaydını netleştirebilir. Kesin tasarım panel ve web yazılımı modeline bağlıdır.

### WooCommerce mağazası diğer sitelerle VPS paylaşabilir mi? {#can-one-woocommerce-store-share-a-vps-with-other-sites}

Paylaşabilir; ancak mağazanın ödeme, veritabanı ve arka plan yoğunlukları baskın yük olabilir. Mağaza iş açısından kritikse veya diğer siteleri sürekli kaynaksız bırakıyorsa ayırın.

### Birden fazla site barındırmak için kontrol paneli daha mı iyidir? {#is-a-control-panel-better-for-hosting-multiple-websites}

Yönetim açısından çoğu zaman evet. Panel alan adlarını, kullanıcıları, SSL'i, PHP'yi, veritabanlarını ve yedekleri kolaylaştırabilir; ancak kullanıcı/hesap yalıtım modelini ve kaynak yükünü doğrulayın.

### Birden fazla site için konteyner gerekli mi? {#are-containers-required-for-multiple-websites}

Hayır. Ayrı kullanıcılar/süreçlerle Nginx/Apache sanal konakları birçok site barındırabilir. Bağımlılık ve süreç yalıtımı ek işletim karmaşıklığını haklı çıkarıyorsa konteyner yararlıdır.

### Birçok siteyi tek VPS'te barındırmanın temel riski nedir? {#what-is-the-main-risk-of-hosting-many-websites-on-one-vps}

Ortak etki alanıdır. Tek kesinti, hatalı güncelleme, dolu disk veya sunucu düzeyinde ele geçirilme o VPS'teki her siteyi etkileyebilir.

### Ajanslar tüm müşterileri tek VPS'e koymalı mı? {#should-agencies-put-all-clients-on-one-vps}

Yalnızca ortak arıza alanını kabul edip güçlü hesap/dosya/veritabanı yalıtımı, yedekler, izleme ve müşteri ayrılış süreçleri uygularlarsa. Kritik veya uyumsuz müşteriler ayrı sunucular gerektirebilir.

### Ne zaman birden fazla VPS sunucusuna ayırmalıyım? {#when-should-i-split-into-multiple-vps-servers}

Tek yük kaynaklara baskın geldiğinde, kritik site bağımsız arıza yalıtımı istediğinde, yazılım/güvenlik sınırları uyumsuz olduğunda veya veritabanı/işçi süreçleri bağımsız ölçeklendirme gerektirdiğinde ayırın.
