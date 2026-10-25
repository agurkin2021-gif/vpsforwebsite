---
title: "WordPress için VPS"
description: "WordPress için VPS: CPU ve RAM'i PHP işçi süreçleri, veritabanı yükü, önbellek, eklentiler ve arka plan görevlerine göre seçin; yönetimi ve taşımayı planlayın."
image: "images/home/vps-for-website-hero.webp"
slug: "wordpress-icin-vps"
---

WordPress için VPS, siteniz paylaşımlı hostingin sağlayabileceğinden daha fazla kontrol, yalıtım veya sunucu özelliği gerektirdiğinde yararlıdır. VPS kaynakları aylık ziyaretçi sayısına değil; **önbelleksiz PHP işlemlerine, veritabanı ihtiyacına, eklentilere, arka plan görevlerine, depolama artışına ve WordPress ile birlikte çalışan servislere** göre seçilmelidir.

Genel sunucu seçimi için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[Kısa yanıt](#quick-answer) · [Uygunluk aracı](#wordpress-vps-fit-checker) · [PHP işçi süreçleri](#php-workers-and-ram) · [Önbellek](#wordpress-caching-layers) · [Veritabanı](#database-demand) · [WP-Cron](#wp-cron-and-background-jobs) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

Bunlar mevcut VDSina Standard paketleri için pratik başlangıç noktalarıdır; ziyaretçi kapasitesi garantisi değildir.

| WordPress iş yükü | Pratik başlangıç noktası | Doğrulanacak temel sınır |
|---|---:|---|
| Laboratuvar/test sitesi veya çok hafif, önbelleklenen WordPress | **1 vCPU / 1 GB / 10 GB** | RAM ve depolama payı çok azdır; canlı ortam için varsayılan hedef değildir |
| Küçük, iyi önbelleklenen WordPress sitesi | **1 vCPU / 2 GB / 40 GB** | PHP işçi süreçleri, veritabanı belleği, eklenti/arka plan yükü |
| Kurumsal WordPress sitesi | **2 vCPU / 4 GB / 80 GB** | eşzamanlı önbelleksiz işlemler, veritabanı gecikmesi, cron/eklentiler |
| Daha ağır dinamik WordPress, büyük veritabanı veya birkaç etkin site | **4 vCPU / 8 GB / 160 GB** | sürekli CPU yükü, PHP kuyruğu, veritabanının etkin veri kümesi, çakışan görevler |

Güncel VDSina Standard fiyatları 13 Ekim 2026 tarihinde yeniden kontrol edildi:

- 1 vCPU / 1 GB / 10 GB / aylık 1 TB veri aktarımı — **$0.07/gün**;
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/gün**;
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/gün**;
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/gün**.

Sitede dinamik sepet, ödeme, hesap, sipariş veya stok işlemleri olan gerçek bir mağaza varsa, onu sıradan önbelleklenen WordPress gibi değerlendirmek yerine [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) rehberini kullanın.

Yazılım bileşenlerini birlikte ele alan daha ayrıntılı hesap için [web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) rehberine bakın.

## WordPress gereksinimleri, VPS kaynak seçimi değildir {#wordpress-requirements-are-not-vps-sizing}

WordPress.org şu özellikleri destekleyen bir hosting ortamını önerir:

- **PHP 8.3 veya üzeri**;
- **MariaDB 10.11+ veya MySQL 8.0+**;
- **HTTPS**;
- önerilen web sunucusu seçenekleri olarak Apache veya Nginx.

Bu gereksinimler **“bu sunucu WordPress çalıştırabilir mi?”** sorusunu yanıtlar. **“Canlı iş yükü ne kadar VPS kaynağı gerektirir?”** sorusunu yanıtlamaz.

Canlı ortamda VPS'in şu bileşenler için de RAM, CPU ve depolamaya ihtiyacı vardır:

- Linux;
- Nginx/Apache;
- PHP-FPM işçi süreçleri;
- MySQL/MariaDB;
- OPcache;
- kullanılıyorsa sayfa/nesne önbelleği;
- kontrol paneli;
- yerel olarak barındırılıyorsa e-posta;
- yedekler;
- cron görevleri;
- kötü amaçlı yazılım/güvenlik taramaları;
- içe/dışa aktarmalar;
- izleme;
- işletim için kapasite payı.

WordPress yazılım gereksinimlerini, canlı ortam kaynak önerisi olarak kullanmayın.

## WordPress VPS uygunluk aracı {#wordpress-vps-fit-checker}

Bu aracı başlangıç noktası olarak kullanın. Gerçek CPU, RAM ve veritabanı ölçümlerinin yerini tutmaz.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="wordpress-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wp-limits" class="form-label">Mevcut hosting gerçek yük altında tekrarlayan sınırlamalar veya eksik özellikler gösteriyor mu?</label>
    <select id="wp-limits" class="form-input">
      <option value="no">Hayır / ölçülmedi</option>
      <option value="some">Ara sıra kaynak baskısı var</option>
      <option value="yes">Tekrarlayan sınırlar var veya VPS'e özgü bir özellik gerekiyor</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-type" class="form-label">WordPress iş yükü</label>
    <select id="wp-type" class="form-input">
      <option value="content">Çoğunlukla önbelleklenen içerik / tanıtım / blog</option>
      <option value="business">Formlar, eklentiler ve yönetim işlemleri olan kurumsal CMS</option>
      <option value="membership">Üyelik / oturum açmış kullanıcılar / kişiselleştirilmiş site</option>
      <option value="store">WooCommerce / işlem yapan mağaza</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-dynamic" class="form-label">Önbelleksiz PHP / yönetim / API yoğunluğu</label>
    <select id="wp-dynamic" class="form-input">
      <option value="low">Düşük</option>
      <option value="medium">Orta</option>
      <option value="high">Yüksek</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-jobs" class="form-label">Ağır eklentiler, içe aktarmalar, taramalar, yedekler veya arka plan görevleri var mı?</label>
    <select id="wp-jobs" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-db" class="form-label">Veritabanı boyutu/etkinliği</label>
    <select id="wp-db" class="form-input">
      <option value="small">Küçük / hafif</option>
      <option value="medium">Orta</option>
      <option value="large">Büyük / yoğun sorgulu</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-panel" class="form-label">Aynı VPS'te kontrol paneli veya yerel e-posta var mı?</label>
    <select id="wp-panel" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-sites" class="form-label">Kaç etkin WordPress sitesi var?</label>
    <select id="wp-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">WordPress VPS ihtiyacını değerlendirin</button>
</form>
<p id="wordpress-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Mümkün olduğunda gerçek iş yükü ölçümlerini kullanın.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("wordpress-vps-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var limits = document.getElementById("wp-limits").value;
    var type = document.getElementById("wp-type").value;
    var dynamic = document.getElementById("wp-dynamic").value;
    var jobs = document.getElementById("wp-jobs").value === "yes";
    var db = document.getElementById("wp-db").value;
    var panel = document.getElementById("wp-panel").value === "yes";
    var sites = document.getElementById("wp-sites").value;

    var score = 0;
    if (type === "business") score += 2;
    if (type === "membership") score += 4;
    if (type === "store") score += 5;
    if (dynamic === "medium") score += 2;
    if (dynamic === "high") score += 4;
    if (jobs) score += 2;
    if (db === "medium") score += 1;
    if (db === "large") score += 3;
    if (panel) score += 1;
    if (sites === "few") score += 2;
    if (sites === "many") score += 4;

    var result;

    if (limits === "no" && type === "content" && dynamic === "low" && score <= 1) {
      result = "MEVCUT HOSTİNGDE KALIN / ÖNCE OPTİMİZASYON: henüz güçlü bir VPS ihtiyacı görünmüyor. Gerçek kaynak sınırları veya gerekli bir sunucu özelliği ortaya çıkana kadar iyi bir paylaşımlı hosting ya da yönetilen WordPress hizmeti daha kolay olabilir.";
    } else if (type === "store") {
      result = "WOOCOMMERCE YOLU: dinamik ödeme, hesap ve sipariş iş yükünü ölçtükten sonra yaklaşık 4 GB RAM veya üzerini başlangıç olarak değerlendirin. WooCommerce için VPS rehberini kullanın; mağaza trafiği, önbelleğe alınmış sıradan WordPress trafiği değildir.";
    } else if (score <= 2) {
      result = "HAFİF İŞ YÜKÜ İÇİN 2 GB BAŞLANGIÇ: 1 vCPU / 2 GB / 40 GB, küçük ve iyi önbelleklenen bir WordPress sitesine uygun olabilir. PHP işçi süreçlerinin belleğini, veritabanı RAM kullanımını, eklentileri ve arka plan görevlerini izleyin.";
    } else if (score <= 7) {
      result = "PRATİK 4 GB BAŞLANGIÇ: 2 vCPU / 4 GB / 80 GB; kurumsal bir WordPress sitesi, PHP işçi süreçleri, veritabanı, önbellek ve düzenli arka plan işleri için daha sağlıklı bir kapasite payı sağlar.";
    } else {
      result = "8 GB VEYA MİMARİYİ YENİDEN DEĞERLENDİRME: 4 vCPU / 8 GB / 160 GB, daha ağır dinamik iş yükü veya birden fazla WordPress sitesi için daha güçlü bir başlangıçtır. Tek site ya da görev kaynakları baskılıyorsa yalnızca VPS'i büyütmek yerine iş yüklerini ayırmayı değerlendirin.";
    }

    if (limits === "no" && type !== "store" && score > 1) {
      result += " Mevcut hosting siteyi gerçekten sınırlamıyorsa taşımadan önce optimizasyon yapıp ölçün.";
    }

    document.getElementById("wordpress-vps-fit-result").textContent = result;
  });
});
</script>

## WordPress gerçekten ne zaman VPS gerektirir? {#when-wordpress-actually-needs-vps}

Bir WordPress sitesi çok yüksek trafik olmadan da VPS gerektirebilir.

Yaygın gerekçeler:

- gerçek kullanıcı yükü altında tekrarlayan CPU/bellek/işlem sınırları;
- özel PHP veya çalışma ortamı yapılandırması ihtiyacı;
- Redis/Memcached ya da başka bir sunucu servisi ihtiyacı;
- ziyaretçiyle tetiklenen zamanlama yerine gerçek sistem cron'u;
- uzun süre çalışan arka plan görevleri;
- özel Nginx/Apache davranışı;
- ortak ve kontrol edilebilir bir ortam gerektiren birkaç site;
- iş yükleri ve hesaplar arasında daha güçlü yalıtım;
- sunucu düzeyinde izleme veya güvenlik duvarı gereksinimleri.

Tek belirti “site yavaş” ise önce [VPS ve paylaşımlı hosting karşılaştırmasını]({{< relref "vps-vs-shared-hosting.md" >}}) inceleyin ve darboğazın WordPress'in kendisi olmadığını doğrulayın.

## WordPress ne zaman VPS gerektirmez? {#when-wordpress-does-not-need-vps}

Şu durumlarda iyi bir paylaşımlı hosting veya yönetilen WordPress hizmetinde kalın:

- site hafif ve kararlıysa;
- önbellekleme çalışıyorsa;
- sağlayıcının kaynak göstergeleri tekrarlayan sınırlar göstermiyorsa;
- özel servis veya root erişimi gerekmiyorsa;
- ekip Linux bakımını üstlenmek istemiyorsa;
- sağlayıcı yedekleme, güvenlik, güncelleme veya test ortamını yeterince iyi yönetiyorsa;
- VPS esas olarak basit bir hosting hizmetini daha fazla işletim işiyle değiştirecekse.

VPS kendiliğinden daha hızlı değildir. Yanlış boyutlandırılmış veya ayarlanmamış bir VPS, WordPress'i iyi bir yönetilen platformdan daha kötü çalıştırabilir.

## PHP işçi süreçleri ve RAM {#php-workers-and-ram}

Önbelleksiz isteklerde PHP-FPM işçi süreçleri, eşzamanlılığı sınırlayan temel etkenlerden biridir.

Her etkin işçi süreç, isteği işlerken bellek tüketir. Daha fazla süreç daha çok eşzamanlı dinamik isteği karşılayabilir; ancak RAM bütçesini artırmadan süreç sayısını yükseltmek şunlara yol açabilir:

- swap kullanımı;
- bellek baskısı;
- OOM nedeniyle süreçlerin sonlandırılması;
- veritabanının kaynak yetersizliği yaşaması;
- sunucu kararsızlığı.

Pratik bir model:

**WordPress RAM ihtiyacı = işletim sistemi + web sunucusu + veritabanı + önbellek + PHP işçi süreçleri + panel/e-posta/görevler + kapasite payı**

Ardından:

**PHP işçi süreç bütçesi = PHP'ye güvenle ayrılabilen RAM / ölçülen ortalama süreç belleği**

MySQL/MariaDB, önbellek veya işletim sistemine bellek bırakmıyorsa teorik azami süreç sayısını yapılandırmayın.

Oturum açmış kullanıcılar, wp-admin, REST/API istekleri, arama, formlar, önizleme ve kişiselleştirilmiş sayfalar tam sayfa önbelleğini daha sık atlar ve PHP işçi süreçlerini kullanır.

## WordPress önbellek katmanları {#wordpress-caching-layers}

Önbellekleme tek bir özellik değildir.

| Katman | Neyi önbellekler? | Temel etkisi |
|---|---|---|
| **PHP OPcache** | derlenmiş PHP bayt kodu | PHP betiklerinin her istekte yeniden derlenmesini önler |
| **Sayfa önbelleği** | oluşturulmuş HTML | çok sayıda anonim sayfa görüntülemesinin WordPress/PHP çalıştırmadan karşılanmasını sağlar |
| **Kalıcı nesne önbelleği** | yeniden kullanılabilir nesneler/sorgu sonuçları | tekrarlayan veritabanı ve uygulama işlerini azaltır |
| **Tarayıcı/CDN önbelleği** | statik veya uç noktadan sunulabilen içerik | kaynak sunucuya tekrarlayan aktarım ve istekleri azaltır |

WordPress'in kendi optimizasyon belgeleri, önbelleklemeyi önemli bir performans aracı olarak önerir. Ancak bu katmanlar farklı sorunları çözer.

Redis'i sayfa önbelleği olarak adlandırmayın. Redis yaygın olarak kalıcı nesne önbelleğinin arka ucu olarak kullanılır; tam sayfa önbelleği ayrı bir katmandır.

## Kalıcı nesne önbelleği ve Redis {#persistent-object-cache-and-redis}

WordPress bir nesne önbelleği API'si içerir; ancak varsayılan önbellek **istekler arasında kalıcı değildir**.

Kalıcı nesne önbelleği için Redis veya Memcached gibi harici bir arka uç/drop-in ve uygun WordPress entegrasyonu gerekir.

Site sürekli maliyetli veritabanı veya nesne işlemleri yapıyorsa yardımcı olabilir; fakat otomatik bir hızlandırma düğmesi değildir.

Redis eklemeden önce:

- site ve veritabanı iş yükünün bundan yararlandığını doğrulayın;
- PHP ve veritabanı için yeterli RAM kaldığını kontrol edin;
- önbellek isabet oranını ve belleği izleyin;
- sayfa önbelleği kararını ayrı değerlendirin.

Verimli tam sayfa önbelleği ve hafif veritabanı yükü olan bir site, Redis'ten dinamik üyelik sitesine veya yoğun sorgulu bir siteye göre daha az yararlanabilir.

## Veritabanı ihtiyacı {#database-demand}

CPU kullanımı belirgin biçimde doygunluğa ulaşmadan önce WordPress performansı veritabanıyla sınırlanabilir.

Şunları kontrol edin:

- yavaş sorgular;
- büyük options/otomatik yüklenen veri kümeleri;
- eklenti meta verileri;
- arama/filtreleme/raporlama sorguları;
- postmeta ağırlıklı iş yükleri;
- veritabanının etkin veri kümesi;
- eşzamanlı yazma işlemleri;
- içe/dışa aktarmalar;
- depolama gecikmesi.

Daha fazla CPU, sorunlu bir sorguyu düzeltmez. Veritabanı gerçekten daha büyük bir etkin veri kümesine ihtiyaç duyuyorsa RAM artırmak yardımcı olabilir; ancak indeks, sorgu ve eklenti iyileştirmelerinin yerini tutmaz.

Önce ölçün, sonra kaynak artırın.

## Eklentiler, temalar ve arka plan görevleri {#plugins-themes-and-background-jobs}

Bir eklenti yalnızca disk alanı tüketmez.

Eklentiler ve temalar şunları ekleyebilir:

- PHP işlemleri;
- veritabanı sorguları;
- harici API çağrıları;
- zamanlanmış görevler;
- önbellek geçersiz kılma;
- yönetim AJAX işlemleri;
- görsel işleme;
- güvenlik taramaları;
- yedekler;
- içe/dışa aktarmalar;
- analitik/günlük kaydı.

Ağır görevler gerçek kullanıcı trafiğiyle çakışabilir.

Mümkünse yedekleri, taramaları, içe aktarmaları ve görsel işleme görevlerini yoğun saatlerin dışında planlayın. Kaynak sıçramasına tek bir eklenti veya görev yol açıyorsa VPS'in küçük olduğunu varsaymadan önce sorunu düzeltin ya da görevin zamanını değiştirin.

## WP-Cron ve arka plan görevleri {#wp-cron-and-background-jobs}

WP-Cron, sistem zamanlayıcısı gibi sürekli çalışmak yerine WordPress istekleriyle tetiklenir.

Bu, sıradan siteler için yeterli olabilir. Zaman açısından hassas veya yoğun iş yüklerinde WordPress'in geliştirici belgeleri, WordPress cron'unu kontrollü aralıklarla çağırmak için işletim sistemi zamanlayıcısının kullanımını açıklar.

Sistem zamanlayıcısına geçerseniz:

- önce yeni tetikleyiciyi oluşturun;
- çalıştığını doğrulayın;
- ancak bundan sonra, planınız bunu içeriyorsa ziyaretçiyle tetiklenen normal WP-Cron davranışını kapatın;
- başarısız görevleri günlüğe kaydedip izleyin.

Başka bir zamanlayıcı olmadan WP-Cron'u devre dışı bırakmayın.

## Depolama, medya, test ortamı ve yedekler {#storage-media-staging-and-backups}

Disk planı, WordPress çekirdeğinden fazlasını kapsamalıdır.

Şunlar için alan ayırın:

- yüklemeler/medya;
- veritabanı;
- eklentiler/temalar;
- günlükler;
- önbellek dosyaları;
- geçici güncelleme dosyaları;
- görsel işleme için geçici alan;
- test ortamı kopyası;
- sunucu dışına aktarılmadan önce yedek arşivleri;
- beklenen büyüme.

Bugün 20 GB kullanan bir site, klonlama, geri yükleme, eklenti güncellemesi veya yedek sıkıştırması sırasında çok daha fazla geçici alana ihtiyaç duyabilir.

Tek yedeğinizi VPS'te tutmayın.

## Manuel yönetim, kontrol paneli veya FASTPANEL? {#manual-control-panel-or-fastpanel}

WordPress, cPanel veya başka bir panel olmadan sorunsuz çalışabilir.

### Manuel Linux yönetimi {#manual-linux}

Şunları istiyorsanız uygundur:

- asgari yazılım kurulumu;
- SSH üzerinden yönetim;
- özel Nginx/Apache/PHP/veritabanı yapılandırması;
- otomasyon veya Git tabanlı dağıtım.

Manuel kurulum için [VPS üzerinde web sitesi yayınlama]({{< relref "how-to-host-a-website-on-vps.md" >}}) rehberini kullanın.

### Genel amaçlı kontrol paneli {#generic-control-panel}

Alan adı, SSL, PHP, veritabanı, kullanıcı, e-posta veya yedek yönetimini tarayıcı üzerinden yapmak yeterince tekrarlayan işi ortadan kaldırıyorsa yararlıdır.

[Kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) rehberini kullanın.

### FASTPANEL {#fastpanel}

FASTPANEL'in resmi iş akışı WordPress sitesi oluşturmayı destekler. VDSina şu anda önceden yapılandırılmış panel seçeneği olarak Ubuntu 22 üzerinde FASTPANEL listeler.

Bu panele özgü kurulum ve kaynak seçimi için [FASTPANEL ile VPS hosting]({{< relref "fastpanel-vps-hosting.md" >}}) rehberini kullanın.

Kontrol paneli yönetimi kolaylaştırır; VPS'i yönetilen hizmete dönüştürmez.

## Yönetilen ve kendi yönettiğiniz WordPress VPS {#managed-vs-self-managed-wordpress-vps}

Kendi yönettiğiniz VPS'te birinin şu işleri üstlenmesi gerekir:

- işletim sistemi/paket güncellemeleri;
- SSH/güvenlik duvarı;
- PHP/web sunucusu güncellemeleri;
- veritabanı yönetimi;
- WordPress/eklenti/tema güncellemeleri;
- yedekler ve geri yükleme testleri;
- izleme;
- olay müdahalesi.

Bu görevleri kimse üstlenmiyorsa WordPress'in veya kontrol panelinin sunucuyu yöneteceğini varsaymak yerine yönetim hizmeti seçin.

[Yönetilen ve yönetilmeyen VPS karşılaştırmasına]({{< relref "managed-vs-unmanaged-vps.md" >}}) bakın.

## WooCommerce farklı bir WordPress iş yüküdür {#woocommerce-is-a-different-wordpress-workload}

WooCommerce aynı WordPress yazılımlarını kullanır, ancak gerçek mağaza trafiği altında farklı davranır.

Sepet, ödeme, hesap, sipariş, stok ve pek çok zamanlanmış işlem dinamiktir; anonim kullanıcılar için önbelleklenen blog sayfaları gibi değerlendirilemez.

Mağaza işlemleri önemliyse, bunlara özgü kaynak seçimi ve işletim modeli için [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) rehberini kullanın.

## Birden fazla WordPress sitesi {#multiple-wordpress-sites}

Birkaç WordPress sitesi şu kaynakları paylaşır:

- CPU;
- RAM;
- veritabanı servisi;
- PHP işçi süreçleri/havuzları;
- depolama;
- cron/arka plan görevlerinin çalışma aralıkları;
- yedekleme süresi;
- arıza alanı.

Az ziyaret edilen, önbellekli on site; yoğun ve dinamik tek bir üyelik sitesinden daha hafif olabilir.

Gerektiğinde ayrı kullanıcılar ve veritabanı erişim bilgileri kullanın; kaynakları alan adı sayısına değil, **toplam en yüksek yüke** göre seçin.

[Birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) rehberine bakın.

## WordPress VPS kaynaklarını ne zaman artırmalı? {#wordpress-vps-upgrade-triggers}

Kaynakları yalnızca gerçek bir sınırı ölçtükten sonra artırın.

Güçlü göstergeler:

- sürekli RAM baskısı, swap kullanımı veya OOM olayları;
- PHP işçi süreçlerinde tekrarlayan kuyruk veya doygunluk;
- önbellek, sorgu ve eklenti optimizasyonundan sonra süren CPU doygunluğu;
- gerçek etkin veri kümesi ihtiyacından kaynaklanan veritabanı gecikmesi;
- güvenli işletim payını aşan depolama büyümesi;
- arka plan görevlerinin canlı trafikle sürekli çakışması;
- birden fazla etkin sitenin ortak kaynakları tüketmesi.

Bu göstergeler sağlıklıyken site yavaşsa, çözüm daha büyük VPS olmayabilir.

## WordPress VPS yayına alma kontrol listesi {#wordpress-vps-launch-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| WordPress çalışma ortamı | desteklenen PHP/veritabanı sürümleri ve HTTPS |
| PHP | FPM/çalışma ortamı yapılandırılmış; süreç sayısı RAM'e uygun |
| Veritabanı | ayrı erişim bilgileri; yavaş sorgu ve etkin veri kümesi riski değerlendirilmiş |
| Önbellek | sayfa/nesne/OPcache katmanları bilinçli seçilmiş |
| Cron | WP-Cron/sistem zamanlaması çalışıyor ve izleniyor |
| Dosyalar | doğru sahiplik; `777` kullanmadan yazılabilen yükleme dizini |
| HTTPS | güvenilir sertifika ve yenileme yöntemi |
| Yedekler | dosyalar ve veritabanı dahil; harici kopya ve geri yükleme yolu var |
| Güncellemeler | işletim sistemi, WordPress, eklenti ve temalar için sorumlu atanmış |
| İzleme | harici erişilebilirlik kontrolü ve CPU/RAM/disk/günlük görünürlüğü |
| Yeniden başlatma | web/PHP/veritabanı/cron otomatik geri geliyor |
| Kapasite | gerçek kullanımı temsil eden önbelleksiz/dinamik yük altında ölçülmüş |

Mevcut canlı site için geçiş, son yazma işlemleri, DNS ve geri dönüş konularında [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberini kullanın.

## Güncel WordPress VPS örnekleri {#current-wordpress-vps-examples}

Bu VDSina Standard yapılandırmaları güncel örneklerdir; WordPress trafik garantisi değildir.

| VPS | Uygun başlangıç kullanımı | Ne zaman yeniden değerlendirmeli? |
|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/gün | laboratuvar/test veya çok hafif, önbellekli WordPress | canlı veritabanı, birkaç PHP işçi süreci ve panel/e-posta olduğunda |
| 1 vCPU / 2 GB / 40 GB — $0.50/gün | hafif, küçük WordPress sitesi | ağır eklentiler, birden fazla etkin site veya sürekli dinamik yük olduğunda |
| 2 vCPU / 4 GB / 80 GB — $0.67/gün | kurumsal WordPress için pratik başlangıç | yoğun üyelik/WooCommerce, büyük veritabanı veya çakışan görevler olduğunda |
| 4 vCPU / 8 GB / 160 GB — $1.34/gün | daha ağır dinamik WordPress / büyük veritabanı / birkaç site | iş yükü bağımsız ölçeklendirme veya daha güçlü yalıtım gerektirdiğinde |

VDSina'nın mevcut Standard sayfası, görünen şablon/uygulama gruplarında WordPress'i özel bir önceden kurulu uygulama olarak listelemiyor. Tek tıklamalı WordPress imajı varsaymak yerine sade işletim sistemiyle manuel kurulumu veya güncel uyumlu bir kontrol panelini kullanın.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel WordPress VPS seçeneklerini inceleyin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Siparişten önce güncel VPS fiyatlarını, şablonları ve panel seçeneklerini doğrulayın.</small></p>

## Teknik kaynaklar {#technical-references}

- WordPress.org — güncel gereksinimler
- WordPress Developer Handbook — önbellekleme
- WordPress Developer — nesne önbelleği
- WordPress Developer — sistem zamanlayıcısı ve WP-Cron
- VDSina Standard VPS

## Sık sorulan sorular {#faq}

### VPS üzerinde WordPress ne kadar RAM gerektirir? {#how-much-ram-does-wordpress-need-on-a-vps}

WordPress çekirdeği, canlı VPS için bir RAM gereksinimi tanımlamaz. RAM; Linux'u, web sunucusunu, PHP işçi süreçlerini, veritabanını, önbellekleri, panel/e-posta/arka plan görevlerini ve kapasite payını karşılamalıdır. Hafif bir site 2 GB'a sığabilir; kurumsal site için 4 GB daha güçlü bir pratik başlangıçtır.

### WordPress VPS için 1 GB RAM yeterli mi? {#is-1-gb-ram-enough-for-wordpress-vps}

Çok hafif bir WordPress kurulumu veya test sitesi çalışabilir; ancak veritabanı, PHP işçi süreçleri ve arka plan işleri için çok az pay kalır. Canlı ortam için olağan öneri olarak değerlendirilmemelidir.

### WordPress için 2 GB RAM yeterli mi? {#is-2-gb-ram-enough-for-wordpress}

Hafif yazılım ortamına sahip, küçük ve iyi önbelleklenen bir site için yeterli olabilir. PHP işçi süreçlerinin belleğini, veritabanı RAM kullanımını, eklentileri ve arka plan görevlerini izleyin.

### WordPress için 4 GB RAM yeterli mi? {#is-4-gb-ram-enough-for-wordpress}

Pek çok kurumsal WordPress sitesi için 4 GB pratik bir başlangıçtır. Ağır eklentiler, üyelik trafiği, WooCommerce, büyük veritabanları, içe aktarmalar veya birkaç etkin site daha fazlasını gerektirebilir.

### WordPress VPS kaç ziyaretçiyi kaldırır? {#how-many-visitors-can-a-wordpress-vps-handle}

Güvenilir, evrensel bir ziyaretçi sayısı yoktur. Kapasiteyi önbellek isabet oranı, eşzamanlı önbelleksiz istekler, PHP istek süresi, eklenti maliyeti, veritabanı işlemleri ve arka plan görevleri belirler.

### VPS'te WordPress için Redis gerekli mi? {#do-i-need-redis-for-wordpress-on-vps}

Hayır. İş yükü tekrarlayan nesne/veritabanı önbelleğinden yararlanıyorsa Redis kalıcı nesne önbelleği sağlayabilir. Her WordPress sitesi için gerekli değildir ve tam sayfa önbelleğinin yerini tutmaz.

### WordPress VPS için Nginx mi Apache mi kullanmalıyım? {#should-i-use-nginx-or-apache-for-wordpress-vps}

İkisi de geçerli seçeneklerdir. WordPress.org Apache veya Nginx'i sağlam seçenekler olarak önerir. Uygulamanızın ve yöneticinizin güvenilir biçimde çalıştırabileceği ortamı kullanın.

### WP-Cron yerine sistem cron'u kullanmalı mıyım? {#should-i-replace-wp-cron-with-system-cron}

Yalnızca iş yükü kontrollü bir zamanlayıcıdan yararlanıyorsa ve çalışan bir alternatif yapılandırdıysanız. Başka bir tetikleyici olmadan WP-Cron'u devre dışı bırakmayın.

### WordPress VPS kontrol paneli gerektirir mi? {#does-wordpress-vps-need-a-control-panel}

Hayır. WordPress, manuel yönetilen bir Linux VPS'te çalışabilir. Panel isteğe bağlıdır; performans gereksinimi olarak değil, yönetim kolaylığı için seçilmelidir.

### VDSina WordPress'i önceden kurulu sunuyor mu? {#does-vdsina-include-wordpress-preinstalled}

Mevcut Standard VPS sayfası, görünen şablon/uygulama gruplarında WordPress'i özel bir önceden kurulu uygulama olarak listelemiyor. Herhangi bir şablonun varlığını varsaymadan önce canlı sipariş ekranını doğrulayın.
