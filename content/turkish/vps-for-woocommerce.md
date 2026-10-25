---
title: "WooCommerce için VPS"
description: "WooCommerce için VPS: CPU ve RAM'i eşzamanlı ödeme işlemleri, PHP süreçleri, veritabanı yazmaları, Action Scheduler, entegrasyonlar ve satış yoğunluğuna göre seçin."
image: "images/home/vps-for-website-hero.webp"
slug: "woocommerce-icin-vps"
---

WooCommerce için VPS, mağazanın önbellekli blog gibi davranamayan bölümlerine göre boyutlandırılmalıdır: **sepet, ödeme, hesap, siparişler, stok, ödeme geri çağrıları, zamanlanmış işlemler ve veritabanı yazmaları**. Yalnızca aylık ziyaret veya ürün sayısı, mağazanın ne kadar sunucu kaynağı istediğini göstermez.

Genel WordPress iş yükü için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberine bakın. Temel sunucu satın alma süreci için [web sitesi için VPS]({{< relref "_index.md" >}}) sayfasını inceleyin.

[Kısa yanıt](#quick-answer) · [Uygunluk aracı](#woocommerce-vps-fit-checker) · [Ödeme yükü](#checkout-and-account-traffic-stay-dynamic) · [Veritabanı](#database-demand-and-hpos) · [Zamanlanmış işlemler](#action-scheduler-and-background-work) · [Satış yoğunlukları](#size-for-sale-and-campaign-peaks) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

Bunlar mevcut VDSina Standard paketleri için pratik başlangıç noktalarıdır; sipariş veya ziyaretçi sayısı garantisi değildir.

| WooCommerce iş yükü | Pratik başlangıç noktası | Doğrulanacak temel sınır |
|---|---:|---|
| Laboratuvar/test mağazası veya çok hafif, düşük hacimli kurulum | **1 vCPU / 2 GB / 40 GB** | PHP, veritabanı ve arka plan görevleri çakıştığında canlı ortam payı çok azalır |
| Küçük işletme mağazası | **2 vCPU / 4 GB / 80 GB** | eşzamanlı ödeme işlemleri, PHP süreçleri, veritabanı gecikmesi, zamanlanmış işlemler |
| Daha ağır mağaza, büyük katalog/veritabanı, fazla entegrasyon veya satış yoğunlukları | **4 vCPU / 8 GB / 160 GB** | sürekli CPU yükü, PHP kuyruğu, veritabanının etkin veri kümesi, Action Scheduler, depolama artışı |
| Tek 8 GB VPS'i aşan yüksek işlem yükü | **Mimariyi yeniden değerlendirin** | yalnızca tek sunucuyu büyütmek yerine veritabanını/işçi süreçlerini/servisleri ayırın veya daha güçlü/bulut/yönetilen mimariye geçin |

WooCommerce'in kendi ölçeklendirme rehberi, OPcache, CDN ve kalıcı önbellek desteğiyle kendi sunucunuzda barındırma için temel kurulum olarak **1 vCPU + en az 2 GB RAM** belirtmiştir. Bu bir başlangıç alt sınırıdır; canlı mağazanın bu kaynaklarla rahat çalışacağına dair vaat değildir.

Güncel VDSina Standard fiyatları 13 Ekim 2026 tarihinde yeniden kontrol edildi:

- 1 vCPU / 1 GB / 10 GB / aylık 1 TB veri aktarımı — **$0.07/gün**;
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/gün**;
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/gün**;
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/gün**.

Birçok gerçek işletme mağazası için **4 GB daha pratik bir başlangıç paketidir**; çünkü VPS aynı anda işletim sistemini, veritabanını, PHP süreçlerini, önbelleği, arka plan görevlerini ve işletim payını karşılamalıdır.

Tüm yazılım bileşenlerini kapsayan ayrıntılı boyutlandırma için [web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) rehberini kullanın.

## WooCommerce gereksinimleri, canlı VPS kaynak seçimi değildir {#woocommerce-requirements-are-not-production-vps-sizing}

WooCommerce 10.8+ için güncel sunucu önerileri şunları gerektirir:

- **WordPress 6.9+**;
- **PHP 8.3+**;
- **MySQL 8.0+ veya MariaDB 10.6+**;
- **HTTPS**;
- **WordPress bellek sınırı 256 MB+**;
- önerilen web sunucusu seçenekleri olarak Apache veya Nginx.

Bu değerler **“ortam WooCommerce'in temel yazılım gereksinimlerini karşılıyor mu?”** sorusunu yanıtlar.

Şu soruları yanıtlamaz:

- kaç PHP işçi süreci gerektiği;
- toplam VPS RAM ihtiyacı;
- veritabanının etkin veri kümesinin belleğe sığıp sığmadığı;
- yük altında ödeme isteklerinin kuyruğa girip girmediği;
- zamanlanmış işlemlerin gecikip gecikmediği;
- yedeklerin/içe aktarmaların müşteri işlemleriyle çakışıp çakışmadığı;
- ödeme/webhook entegrasyonlarının istekleri geciktirip geciktirmediği.

**256 MB WordPress/PHP bellek sınırı, 256 MB VPS RAM'i demek değildir**. Toplam sunucu RAM'i Linux'u, web sunucusunu, veritabanını, PHP süreçlerini, önbelleği, görevleri, panel/e-postayı ve kapasite payını da karşılamalıdır.

## WooCommerce VPS uygunluk aracı {#woocommerce-vps-fit-checker}

Bunu performans garantisi olarak değil, başlangıç kararı için kullanın.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="woocommerce-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wc-stage" class="form-label">Mağazanın aşaması / iş açısından önemi</label>
    <select id="wc-stage" class="form-input">
      <option value="test">Test / yayına hazırlık / düşük ticari etki</option>
      <option value="small">Küçük, yayındaki mağaza</option>
      <option value="business">İş açısından kritik mağaza</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-limits" class="form-label">Mevcut hosting tekrarlayan kaynak sınırları veya eksik özellikler gösteriyor mu?</label>
    <select id="wc-limits" class="form-input">
      <option value="no">Hayır / ölçülmedi</option>
      <option value="yes">Evet</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-external" class="form-label">Temel arıza/gecikmenin ödeme, kargo, vergi, SMTP veya başka bir harici servisten kaynaklandığı belirlendi mi?</label>
    <select id="wc-external" class="form-input">
      <option value="no">Hayır / bilinmiyor</option>
      <option value="yes">Evet</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-checkout" class="form-label">Eşzamanlı ödeme/hesap işlemleri</label>
    <select id="wc-checkout" class="form-input">
      <option value="low">Düşük</option>
      <option value="medium">Orta</option>
      <option value="high">Yüksek / kampanya kaynaklı</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-catalog" class="form-label">Katalog / arama / filtreleme iş yükü</label>
    <select id="wc-catalog" class="form-input">
      <option value="light">Hafif</option>
      <option value="medium">Orta</option>
      <option value="heavy">Büyük / yoğun sorgulu</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-jobs" class="form-label">Ağır eklentiler, içe aktarmalar, webhook'lar, abonelikler veya zamanlanmış görevler var mı?</label>
    <select id="wc-jobs" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-db" class="form-label">Veritabanı / sipariş etkinliği</label>
    <select id="wc-db" class="form-input">
      <option value="small">Küçük / hafif</option>
      <option value="medium">Orta</option>
      <option value="heavy">Yoğun yazma/sorgu etkinliği</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-panel" class="form-label">Aynı VPS'te kontrol paneli veya yerel e-posta var mı?</label>
    <select id="wc-panel" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-spikes" class="form-label">Düzenli indirim/bülten/promosyon yoğunlukları oluyor mu?</label>
    <select id="wc-spikes" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-operator" class="form-label">VPS işletimini üstlenebilecek biri var mı?</label>
    <select id="wc-operator" class="form-input">
      <option value="no">Hayır</option>
      <option value="help">Yalnızca yönetilen hizmet / ücretli yönetim desteğiyle</option>
      <option value="yes">Evet</option>
    </select>
  </div>
  <button class="btn btn-primary" type="submit">WooCommerce VPS ihtiyacını değerlendirin</button>
</form>
<p id="woocommerce-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Mağazanızı en iyi temsil eden iş yükünü seçin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("woocommerce-vps-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var stage = val("wc-stage");
    var limits = val("wc-limits") === "yes";
    var external = val("wc-external") === "yes";
    var checkout = val("wc-checkout");
    var catalog = val("wc-catalog");
    var jobs = val("wc-jobs") === "yes";
    var db = val("wc-db");
    var panel = val("wc-panel") === "yes";
    var spikes = val("wc-spikes") === "yes";
    var operator = val("wc-operator");

    var score = 0;
    if (stage === "small") score += 1;
    if (stage === "business") score += 3;
    if (checkout === "medium") score += 2;
    if (checkout === "high") score += 4;
    if (catalog === "medium") score += 1;
    if (catalog === "heavy") score += 3;
    if (jobs) score += 2;
    if (db === "medium") score += 1;
    if (db === "heavy") score += 3;
    if (panel) score += 1;
    if (spikes) score += 2;

    var result;

    if (external) {
      result = "ÖNCE HARİCİ SERVİSİ / UYGULAMAYI İNCELEYİN: temel arızanın VPS kaynak havuzu dışında olduğu belirlenmiş. Daha fazla CPU veya RAM almadan önce ödeme geçidi, API, SMTP veya entegrasyon yolunu düzeltin ya da ölçün.";
    } else if (!limits && stage !== "business" && score <= 2) {
      result = "YÖNETİLEN / PAYLAŞIMLI HOSTİNG HÂLÂ UYGUN OLABİLİR: henüz VPS gerektiren ölçülmüş bir sınır yok. Gerçek bir kaynak veya özellik ihtiyacı ortaya çıkana kadar daha basit hosting modelini koruyun ya da önce optimizasyon yapın.";
    } else if (stage === "business" && operator !== "yes") {
      result = "YÖNETİLEN HİZMET / YÖNETİM DESTEĞİ YOLU: mağaza iş açısından kritik ve sunucu işletiminin tümünü üstlenen kurum içi sorumlu yok. Yönetilmeyen yalın bir VPS seçmeden önce yönetilen hizmet veya ücretli yönetim desteği kullanın.";
    } else if (score <= 2) {
      result = "HAFİF 2 GB / KÜÇÜK MAĞAZA YOLU: 1 vCPU / 2 GB / 40 GB çok hafif bir mağaza için temel başlangıç olabilir. Canlı kullanıma hazır saymadan önce ödeme akışını, PHP süreçlerinin belleğini, veritabanı gecikmesini ve zamanlanmış işlemleri doğrulayın.";
    } else if (score <= 7) {
      result = "PRATİK 4 GB BAŞLANGIÇ: 2 vCPU / 4 GB / 80 GB; dinamik ödeme, veritabanı yazmaları ve olağan arka plan işleri olan küçük bir WooCommerce işletmesi için daha sağlıklı kapasite payı sağlar.";
    } else {
      result = "8 GB VEYA MİMARİYİ YENİDEN DEĞERLENDİRME: 4 vCPU / 8 GB / 160 GB, daha ağır mağazalar veya satış yoğunlukları için daha güçlü başlangıçtır. Veritabanı, görevler veya entegrasyonlar baskınsa iş yüklerini ayırmayı ya da daha güçlü bir yönetilen/bulut mimarisini değerlendirin.";
    }

    document.getElementById("woocommerce-vps-fit-result").textContent = result;
  });
});
</script>

## WooCommerce gerçekten ne zaman VPS gerektirir? {#when-woocommerce-actually-needs-vps}

Şu durumlarda WooCommerce mağazası için VPS gerekçelendirilebilir:

- paylaşımlı hosting gerçek yük altında sürekli CPU/bellek/işlem/G/Ç sınırlarına takılıyorsa;
- gerçek yük altında ödeme/hesap istekleri kuyruğa giriyorsa;
- veritabanının etkin veri kümesi veya yazma yükü daha fazla kontrol gerektiriyorsa;
- eklentiler mevcut hostingin izin vermediği servisleri gerektiriyorsa;
- Redis/Memcached veya özel sunucu yapılandırması gerekiyorsa;
- Action Scheduler/arka plan görevleri daha güvenilir çalıştırma gerektiriyorsa;
- ürün içe aktarmaları, veri akışları veya stok eşitlemesi müşteri trafiğiyle çakışıyorsa;
- özel PHP/çalışma ortamı/web sunucusu ayarları gerekiyorsa;
- test ortamı veya mağazaya özgü işletim kontrolü gerekiyorsa.

Mağaza küçük, kararlı ve yönetilen WooCommerce/WordPress hostinginde iyi destekleniyorsa VPS kendiliğinden daha iyi seçenek değildir.

## Yönetilen WooCommerce hosting ne zaman daha iyi olabilir? {#when-managed-woocommerce-hosting-may-be-better}

Şu durumlarda kendi yönettiğiniz VPS uygun değildir:

- işletim sistemi/güvenlik güncellemelerini kimse üstlenmiyorsa;
- ödeme erişilebilirliğini veya sunucu uyarılarını kimse izlemiyorsa;
- yedekler varsa ama geri yükleme test edilmemişse;
- ödeme/sipariş kesintisi iş açısından kritikse;
- ekip Linux yönetimi yerine WordPress/WooCommerce desteği istiyorsa;
- mevcut yönetilen platform performans ve ölçeklendirmeyi zaten yeterince karşılıyorsa.

VPS daha fazla kontrol sağlayabilir; aynı zamanda üstlenmeniz gereken arıza türlerini de artırır.

Gelir açısından kritik mağazayı kendi yönettiğiniz sunucuya taşımadan önce [yönetilen ve yönetilmeyen VPS karşılaştırmasına]({{< relref "managed-vs-unmanaged-vps.md" >}}) bakın.

## Ödeme ve hesap trafiği dinamiktir {#checkout-and-account-traffic-stay-dynamic}

WooCommerce'in kendi önbellekleme rehberi, müşteriye özgü durum bilgisi içerdikleri için **Sepet, Hesabım ve Ödeme** sayfalarının tam sayfa önbelleğinden hariç tutulmasını söyler.

Bu önemlidir; çünkü ticari açıdan en önemli isteklerde hâlâ şu işlemler yürütülebilir:

- PHP;
- oturum/sepet mantığı;
- kargo/vergi hesaplamaları;
- ödeme entegrasyonu kodu;
- veritabanı okuma/yazmaları;
- sipariş oluşturma;
- stok güncellemeleri;
- kancalar/eklentiler.

Bu nedenle mağaza önbellekli ürün sayfasını hızla sunarken ödeme istekleri yine de kuyruğa girebilir.

WooCommerce kaynaklarını yalnızca kataloğun önbellek isabet oranına göre seçmeyin.

## PHP işçi süreçleri ve dinamik eşzamanlılık {#php-workers-and-dynamic-concurrency}

Dinamik WooCommerce isteklerinde PHP işçi süreçleri, aynı anda kaç isteğin yürütülebileceğini belirler.

Yararlı bir yaklaşık hesap:

**etkin dinamik istekler ≈ saniyedeki önbelleksiz istekler × istek süresi**

Yoğun saatte ödeme/hesap/API istekleri ortalama 0.8 saniye sürüyorsa ve PHP'ye saniyede 5 dinamik istek ulaşıyorsa; yönetim işlemleri, webhook'lar veya arka plan görevleri eklenmeden yaklaşık dört süreç aynı anda meşgul olabilir.

Her süreç bellek tüketir. RAM bütçesi olmadan süreç sayısını artırmak veritabanını kaynaksız bırakabilir veya sunucuyu swap/OOM durumuna sürükleyebilir.

Şu modeli kullanın:

**WooCommerce RAM ihtiyacı = işletim sistemi + web sunucusu + veritabanı + önbellek + PHP süreçleri + görevler + panel/e-posta + kapasite payı**

Ardından genel bir süreç sayısını kopyalamak yerine ortalama ve en yüksek süreç belleğini doğrulayın.

## WooCommerce'i doğru önbellekleyin {#cache-woocommerce-correctly}

WooCommerce katmanlı bir önbellek stratejisi gerektirir.

### Tam sayfa önbelleği {#full-page-cache}

Önbelleğe alınabilir katalog/içerik sayfaları için yararlıdır.

Şunları bilinçsizce önbelleğe **almayın**:

- Sepet;
- Ödeme;
- Hesabım;
- müşteriye/oturuma özgü yanıtlar.

WooCommerce'in resmi önbellekleme rehberi bu sayfaları açıkça hariç tutar.

### OPcache {#opcache}

Derlenmiş PHP bayt kodunu önbellekler ve tekrarlayan PHP derleme işini azaltır.

### Kalıcı nesne önbelleği {#persistent-object-cache}

İş yükü yararlanıyorsa Redis veya Memcached tekrarlayan veritabanı/nesne işlemlerini azaltabilir.

Tam sayfa önbelleğinin yerini tutmaz ve verimsiz sorguları kendiliğinden düzeltmez.

### Tarayıcı / CDN {#browser--cdn}

Statik dosyalar ve uç noktadan sunulabilen içerik için yararlıdır.

CDN, kaynak sunucuya giden statik istekleri azaltabilir; ancak dinamik ödeme/veritabanı işlemlerini ortadan kaldırmaz.

## Veritabanı ihtiyacı ve HPOS {#database-demand-and-hpos}

WooCommerce, sıradan önbellekli WordPress sitesine göre daha yoğun veritabanı okuma/yazma davranışı oluşturur.

Önemli veritabanı işleri şunları içerebilir:

- sipariş oluşturma ve güncelleme;
- müşteri/hesap verileri;
- stok değişiklikleri;
- ürün/katalog sorguları;
- oturumlar;
- eklenti meta verileri;
- raporlar/analitik;
- arama/filtreleme;
- zamanlanmış görevler.

WooCommerce **High-Performance Order Storage (HPOS)**, sipariş verilerini özel tablolarda saklar ve WooCommerce 8.2'den itibaren yeni kurulumlarda varsayılan olarak etkindir.

HPOS önemli bir mimari iyileştirmedir; ancak şunların yerini tutmaz:

- uyumlu eklentiler/özel kod;
- sorgu/indeks incelemesi;
- yeterli veritabanı belleği;
- düşük depolama gecikmesi;
- izleme;
- büyük değişikliklerden önce test ortamı ve doğrulama.

WooCommerce, mevcut büyük mağazalarda canlı geçişten önce HPOS taşımasının ve kritik akışların test edilmesini önerir.

## Action Scheduler ve arka plan işleri {#action-scheduler-and-background-work}

WooCommerce şu arka plan görevleri için **Action Scheduler** kullanır:

- sipariş bildirimleri;
- ödemeyle ilgili işlemler;
- webhook'lar;
- abonelikler/yenilemeler;
- eklenti görevleri;
- içe aktarma/eşitleme.

WooCommerce bunları **WooCommerce > Durum > Zamanlanmış Eylemler** altında gösterir.

Şunları izleyin:

- başarısız işlemler;
- zamanı geçmiş işlemler;
- sürekli biriken bekleyen işlemler;
- uzun süren görevler;
- müşteri yoğunluğunda büyüyen kuyruklar.

Action Scheduler varsayılan olarak WordPress zamanlamasına bağlıdır; bu nedenle güvenilir zamanlama gerektiğinde sunucu tarafı cron yararlı olabilir.

Önbellekli sayfaları hızlı olan bir mağazada bile zamanlanmış işlem kuyruğu çalışmıyorsa işletim sorunları yaşanabilir.

## Ödemeler, webhook'lar, e-posta ve entegrasyonlar {#payments-webhooks-email-and-integrations}

Daha büyük VPS, her ödeme hatasını düzeltemez.

Harici bağımlılıklar şunları içerebilir:

- ödeme geçitleri;
- vergi API'leri;
- kargo API'leri;
- stok/ERP eşitlemesi;
- CRM;
- işlem e-postaları;
- dolandırıcılık kontrolleri;
- webhook'lar;
- harici arama/servisler.

Gecikmenin VPS'inizden mi yoksa harici servisten mi kaynaklandığını ölçün.

Şunları izleyin:

- başarısız ödeme geri çağrıları;
- webhook teslimatı;
- e-posta kuyrukları;
- API zaman aşımları;
- yeniden deneme ve bekleme süresi artırma davranışı;
- Action Scheduler hataları.

Üçüncü taraf API darboğazını çözmek için CPU satın almayın.

## Katalog, arama ve filtreleme {#catalog-search-and-filtering}

Büyük kataloglar yalnızca çok ürün içerdiği için yük oluşturmaz.

Asıl baskı şunlardan gelir:

- karmaşık arama/filtre sorguları;
- özellik/taksonomi sorguları;
- ürün arama tabloları;
- varyasyon sayıları;
- fiyatlandırma/stok kuralları;
- SQL veya harici çağrı ekleyen eklentiler;
- önbelleğe alınmamış kişiselleştirilmiş sonuçlar.

Arama/filtreleme uç noktalarını normal ürün sayfası gezinmesinden ayrı ölçün.

Kalıcı önbellek bazı tekrarlayan sorgulara yardımcı olabilir; ancak veritabanı ve sorgu tasarımı önemini korur.

## Satış ve kampanya yoğunluklarına göre kaynak seçin {#size-for-sale-and-campaign-peaks}

WooCommerce'in en yüksek yükü çoğu zaman birkaç işi aynı anda birleştirir:

- bülten/reklam trafiği;
- katalogda gezinme;
- sepete ekleme;
- ödeme;
- ödeme geri çağrıları;
- sipariş e-postaları;
- stok güncellemeleri;
- yönetim/sipariş işleme;
- webhook'lar;
- zamanlanmış işlemler;
- analitik/günlük kaydı.

Ortalama güne değil, **gerçek kullanımı temsil eden yoğun zaman aralığına** göre kaynak seçin.

Büyük bir promosyondan önce:

1. gerçek kullanımı temsil eden ödeme trafiğini test edin;
2. PHP işçi süreçlerinin kapasite payını doğrulayın;
3. veritabanı gecikmesini ve bağlantılarını doğrulayın;
4. Action Scheduler birikimini kontrol edin;
5. içe aktarma/yedekleme/tarama işlerini duraklatın veya yeniden zamanlayın;
6. harici ödeme/kargo/vergi API'lerini doğrulayın;
7. kampanya sırasında günlükleri ve kaynak metriklerini izleyin.

## Depolama, yedekler ve test ortamı {#storage-backups-and-staging}

WooCommerce yedeği hem dosyaları hem işlem verilerini korumalıdır.

Şunları dahil edin:

- WordPress/WooCommerce dosyaları;
- yüklemeler/ürün görselleri;
- veritabanı/sipariş verileri;
- kurtarma için gereken yapılandırma ve gizli bilgiler;
- eklenti/tema/özel kod;
- entegrasyon ayarları.

### İşlem verilerini dikkate alan kurtarma {#transaction-aware-recovery}

Mağaza sürekli sipariş alıyorsa yedekleme sıklığı, olası sipariş verisi kaybını belirler.

Günlük veritabanı yedeği, son işlemlerin bir güne kadar olan bölümünün bu geri yükleme noktasının dışında kalması anlamına gelebilir.

Yedekleme sıklığını kolaylığa değil, kabul edilebilir **kurtarma noktası hedefine (RPO)** göre seçin.

Ayrıntılı yedekleme mimarisi için [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}}) rehberine bakın.

### Test ortamı {#staging}

Mümkünse PHP, WooCommerce, eklenti, tema, HPOS ve ödeme değişikliklerini canlıya almadan önce test ortamında doğrulayın.

Test kopyaları disk ve bazen veritabanı, RAM, yedekleme kaynaklarını da tüketir; kapasite planına bunları dahil edin.

## Kontrol paneli, FASTPANEL veya manuel kurulum {#control-panel-fastpanel-or-manual-stack}

WooCommerce, manuel yönetilen Linux VPS'te veya hosting kontrol paneli üzerinden çalışabilir.

Genel panel seçimi için [kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) rehberine bakın.

VDSina'da FASTPANEL kullanımına özgü yol için [FASTPANEL ile VPS hosting]({{< relref "fastpanel-vps-hosting.md" >}}) rehberine bakın.

Manuel Linux kurulumu için [VPS üzerinde web sitesi yayınlama]({{< relref "how-to-host-a-website-on-vps.md" >}}) rehberine bakın.

Kontrol paneli rutin işleri kolaylaştırır; ödeme güvenilirliğinin, WooCommerce/eklenti güncellemelerinin, veritabanı ayarlarının, yedeklerin veya olay müdahalesinin sorumluluğunu üstlenmez.

## Canlı mağaza taşımasında veri geçiş noktası belirlenmelidir {#live-store-migration-has-a-data-boundary}

WooCommerce taşıması yalnızca “dosyaları ve veritabanını kopyalamak” değildir.

Mağaza yayındayken siparişler, stok, sepetler, müşteriler ve zamanlanmış işlemler değişebilir.

Taşıma sırasında:

- önce hedef ortamı kurup test edin;
- son yazma işlemlerini kontrol edin;
- son veritabanı/yükleme eşitlemesini çalıştırın;
- yazılabilir iki canlı mağazanın verilerinin birbirinden ayrışmasını önleyin;
- ödeme/webhook uç noktalarını doğrulayın;
- e-posta/DNS düzenini koruyun;
- geri dönüş planını hazır tutun.

Tüm geçiş süreci için [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberini kullanın.

## WooCommerce VPS kaynaklarını ne zaman artırmalı? {#woocommerce-vps-upgrade-triggers}

Ölçümler şunları gösterdiğinde kaynak artırın veya mimariyi değiştirin:

- tekrarlayan PHP süreç kuyrukları;
- önbellek, sorgu ve eklenti optimizasyonundan sonra süren CPU doygunluğu;
- RAM baskısı, swap kullanımı veya OOM;
- veritabanı gecikmesi / etkin veri kümesi baskısı;
- kapasite nedeniyle Action Scheduler birikimi veya hataları;
- gerçek yoğun yük altında ödeme hataları;
- güvenli kapasite payını azaltan depolama artışı;
- yedekleme/içe aktarma/tarama görevlerinin müşteri işlemleriyle çakışması;
- birden fazla mağaza veya servisin tek VPS için rekabet etmesi.

Sunucu kaynakları sağlıklıyken ödeme yavaşsa daha büyük VPS almadan önce ödeme, API, eklenti ve veritabanı nedenlerini araştırın.

## WooCommerce VPS yayına alma kontrol listesi {#woocommerce-vps-launch-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| WooCommerce çalışma ortamı | güncel ve uyumlu WordPress/PHP/veritabanı ile HTTPS |
| PHP belleği | WooCommerce/WordPress bellek sınırı ayarlı; toplam VPS RAM'i ayrıca yeterli |
| PHP işçi süreçleri | gerçek ödeme/hesap eşzamanlılığını temsil eden yük için yeterli |
| Sayfa önbelleği | sepet/ödeme/hesap/oturuma özgü akışlar hariç tutulmuş |
| Nesne önbelleği/OPcache | katmanlar bilinçli seçilmiş; Redis/Memcached yalnızca yarar sağlıyorsa kullanılıyor |
| Veritabanı | sipariş/katalog/sorgu yükü izleniyor; HPOS uyumluluğu değerlendirilmiş |
| Zamanlanmış işlemler | açıklanamayan başarısız/gecikmiş işlem birikimi yok |
| Ödemeler | test siparişleri, ödemeler, iadeler ve webhook'lar başarılı |
| Stok | stok değişiklikleri tutarlı |
| E-posta | işlem mesajları güvenilir bir yoldan teslim ediliyor |
| Yedekler | dosyalar, veritabanı, son siparişler için RPO ve geri yükleme yolu tanımlı |
| Test ortamı | kritik güncellemeler canlı ortam dışında test edilebiliyor |
| İzleme | harici ödeme/site kontrolleri ile CPU/RAM/disk/veritabanı görünürlüğü |
| Yeniden başlatma | web/PHP/veritabanı/görevler otomatik geri geliyor |
| Yoğunluk | gerçek satış/kampanya yükünü temsil eden trafik doğrulanmış |

## Güncel WooCommerce VPS örnekleri {#current-woocommerce-vps-examples}

Bu güncel VDSina Standard paketleri, ihtiyaca eşleme örnekleridir; mağaza kapasitesi garantisi değildir.

| VPS | Uygun başlangıç kullanımı | Ne zaman yeniden değerlendirmeli? |
|---|---|---|
| 1 vCPU / 2 GB / 40 GB — $0.50/gün | laboratuvar/çok hafif küçük mağaza veya kontrollü düşük hacimli kurulum | iş açısından kritik ödeme, ağır eklentiler veya çok görev olduğunda |
| 2 vCPU / 4 GB / 80 GB — $0.67/gün | küçük işletme WooCommerce mağazası için pratik başlangıç | yoğun satış sıçramaları, büyük veritabanı/katalog veya çok entegrasyon olduğunda |
| 4 vCPU / 8 GB / 160 GB — $1.34/gün | daha ağır mağaza / veritabanı, PHP ve arka plan işleri için ek pay | tek sunucu mimarisi darboğaz veya ortak arıza riski haline geldiğinde |

1 GB Standard paket, WooCommerce canlı ortamı için olağan seçenek olarak sunulmaz.

VDSina'nın mevcut Standard sayfası, görünen şablon/uygulama gruplarında özel bir önceden kurulu WooCommerce uygulaması **listelemiyor**. Tek tıklamalı WooCommerce varsaymak yerine uyumlu WordPress, manuel kurulum veya panel yolunu kullanın.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel WooCommerce VPS seçeneklerini inceleyin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Siparişten önce güncel VPS fiyatlarını, şablonları ve panel seçeneklerini doğrulayın.</small></p>

## Teknik kaynaklar {#technical-references}

- WooCommerce — sunucu önerileri
- WooCommerce Developer — WooCommerce ile ölçeklendirme
- WooCommerce Developer — önbellek eklentilerini yapılandırma
- WooCommerce — Zamanlanmış Eylemler
- WooCommerce Developer — High Performance Order Storage
- VDSina Standard VPS

## Sık sorulan sorular {#faq}

### VPS üzerinde WooCommerce ne kadar RAM gerektirir? {#how-much-ram-does-woocommerce-need-on-a-vps}

Evrensel bir değer yoktur. WooCommerce'in ölçeklendirme rehberi, kendi sunucunuzda temel kurulum için 2 GB kullanmıştır. PHP süreçleri, veritabanı, önbellek ve görevler birlikte çalışacağından birçok işletme mağazası için 4 GB VPS daha güçlü bir pratik başlangıçtır.

### WooCommerce için 2 GB RAM yeterli mi? {#is-2-gb-ram-enough-for-woocommerce}

Çok küçük/hafif mağaza veya kontrollü düşük hacimli kurulum için yeterli olabilir. Canlı kullanıma hazır saymadan önce eşzamanlı ödeme yükünü, veritabanı gecikmesini, zamanlanmış işlemleri ve bellek baskısını doğrulayın.

### WooCommerce için 4 GB RAM yeterli mi? {#is-4-gb-ram-enough-for-woocommerce}

Pek çok küçük işletme mağazası için 4 GB pratik bir başlangıçtır. Yoğun trafik, büyük katalog/veritabanı, çok entegrasyon, abonelikler, içe aktarmalar veya satış sıçramaları daha fazlasını gerektirebilir.

### WooCommerce neden normal WordPress'ten daha ağırdır? {#why-is-woocommerce-heavier-than-normal-wordpress}

Sepet, ödeme, hesap, sipariş, stok ve birçok entegrasyon dinamiktir. Herkese açık katalog/içerik sayfaları önbelleklense bile bu istekler PHP ve veritabanı işlemleri yürütür.

### WooCommerce ödeme sayfasını önbelleğe alabilir miyim? {#can-i-cache-woocommerce-checkout}

Müşteriye özgü durum bilgisi içerdiğinden Sepet, Ödeme ve Hesabım tam sayfa önbelleğinden hariç tutulmalıdır. Uygun veri ve içerikler için diğer önbellek katmanlarını kullanın.

### WooCommerce Redis gerektirir mi? {#does-woocommerce-need-redis}

Hayır. İş yükü yararlanıyorsa Redis veya Memcached kalıcı nesne önbelleği sağlayabilir. Doğru sayfa önbelleği istisnalarının veya verimli sorguların yerini tutmaz.

### HPOS nedir? {#what-is-hpos}

High-Performance Order Storage, WooCommerce siparişlerini özel tablolarda saklar. WooCommerce 8.2'den itibaren yeni kurulumlarda varsayılan olarak etkindir. Mevcut mağazada değişiklik yaparken eklenti/özel kod uyumluluğunu ve kritik mağaza akışlarını test edin.

### WooCommerce Zamanlanmış Eylemler nedir? {#what-are-woocommerce-scheduled-actions}

Sipariş bildirimleri, ödemeyle ilgili işlemler, webhook'lar ve eklenti görevleri gibi işler için Action Scheduler'ın yönettiği kuyruklanmış arka plan görevleridir. Başarısız veya gecikmiş kuyruklar işletim sorunu göstergesidir.

### VDSina WooCommerce'i önceden kurulu sunuyor mu? {#does-vdsina-include-woocommerce-preinstalled}

Mevcut VDSina Standard sayfası, görünen şablon/uygulama gruplarında WooCommerce'i özel bir önceden kurulu uygulama olarak listelemiyor. Herhangi bir şablonun varlığını varsaymadan önce canlı sipariş arayüzünü doğrulayın.

### WooCommerce için VPS her zaman yönetilen hostingden daha mı iyidir? {#is-a-vps-always-better-for-woocommerce-than-managed-hosting}

Hayır. Kontrol ve kaynak ihtiyacınız varsa, sunucuyu da yönetebiliyorsanız kendi yönettiğiniz VPS yararlıdır. Mağaza iş açısından kritikse ve kurum içinde sunucu yönetimi sorumlusu yoksa yönetilen WooCommerce/WordPress hosting daha güvenli olabilir.
