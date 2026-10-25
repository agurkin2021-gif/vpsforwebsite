---
title: "Web sitesi için VPS kaynak seçimi"
description: "Web sitesi için VPS kaynak seçimi: CPU, RAM ve depolamayı gerçek iş yükü, hosting sınırları, PHP süreçleri, veritabanı ihtiyacı ve yoğun saat trafiğine göre hesaplayın."
image: "images/home/vps-for-website-hero.webp"
slug: "web-sitesi-icin-vps-kaynak-secimi"
---

Web sitesi için VPS kaynak seçimi, aylık ziyaretçi sayısıyla değil kaynak sunucuya ulaşan iş yüküyle başlamalıdır. Önbelleğe alınabilirlik, eşzamanlı dinamik istekler, PHP veya uygulama işçi süreçleri, veritabanı etkinliği, arka plan görevleri, kontrol paneli yükü ve depolama artışı; sitenin gerçekten ne kadar CPU, RAM ve disk gerektirdiğini belirler.

Genel satın alma kararı için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[RAM hesabına geçin](#ram-budget) · [Paylaşımlı hosting teşhisi](#shared-hosting-to-vps-diagnostic) · [Paket eşleştirme](#match-the-result-to-a-vps) · [Sık sorulan sorular](#faq)

## Kaynak seçimine kısa yanıt {#quick-sizing-answer}

Bu güncel VDSina Standard yapılandırmaları yararlı referans paketlerdir; ancak paketi iş yükü belirlemelidir. Aşağıdaki sağlayıcı değerleri 13 Ekim 2026 tarihinde kontrol edildi.

| Web sitesi iş yükü | Başlangıç VPS örneği | Doğrulanacak noktalar |
|---|---:|---|
| Çok hafif site, test ortamı, kapsamlı önbelleklenen proje | 1 vCPU / 1 GB RAM / 10 GB — $0.07/gün, 1 TB/ay veri aktarımı | Bellek payı, veritabanı boyutu, swap kullanımı |
| Küçük site veya hafif CMS | 1 vCPU / 2 GB RAM / 40 GB — $0.50/gün, 32 TB/ay veri aktarımı | PHP işçi süreçleri, panel yükü, veritabanı belleği |
| Kurumsal site veya tipik dinamik WordPress yükü | 2 vCPU / 4 GB RAM / 80 GB — $0.67/gün, 32 TB/ay veri aktarımı | Eşzamanlı önbelleksiz işlemler, cron görevleri, veritabanı gecikmesi |
| Daha ağır dinamik site, büyük veritabanı veya birkaç etkin site | 4 vCPU / 8 GB RAM / 160 GB — $1.34/gün, 32 TB/ay veri aktarımı | Sürekli CPU yükü, süreç belleği, yoğunlukların çakışması |

Bunlar kaynak seçimi yönlendirmeleridir; trafik garantisi değildir. Aynı ziyaretçi sayısına sahip iki site çok farklı sunucular gerektirebilir. Fiyatlar, veri aktarım kotaları ve diğer sağlayıcı koşulları değişebilir; siparişten önce güncel teklifi doğrulayın.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS yapılandırmalarını inceleyin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Kaynak önerisi komisyona değil, iş yüküne dayanır.</small></p>

## Kaynak modeli: trafiği saymadan önce bileşenlere kaynak ayırın {#the-sizing-model-reserve-resources-before-counting-traffic}

Yararlı bir VPS bütçesi, sunucuyu kaynak tüketen bileşenlerine ayırır.

### RAM bütçesi {#ram-budget}

Toplam RAM şunları karşılamalıdır:

1. işletim sistemi ve sistem servisleri;
2. web sunucusu veya ters proxy;
3. PHP-FPM, Node.js, Python veya başka bir uygulama çalışma ortamı;
4. veritabanı;
5. kullanılıyorsa Redis gibi önbellek servisleri;
6. kontrol paneli ve servisleri;
7. izleme, güvenlik ve yedekleme süreçleri;
8. eşzamanlı uygulama işçi süreçleri;
9. ani yükler, dağıtımlar ve bakım için güvenli kapasite payı.

CMS bellek sınırını sunucunun RAM gereksinimi olarak görmeyin. 256 MB PHP bellek sınırı, 1 GB VPS'in Linux, veritabanı ve diğer servislerle birlikte dört eşzamanlı 256 MB PHP sürecini güvenle çalıştırabileceği anlamına gelmez.

Pratik bir model:

**gerekli RAM = temel servisler + veritabanı çalışma belleği + eşzamanlı süreç belleği + arka plan görevi belleği + kapasite payı**

Mümkün olduğunda gerçek süreçleri ölçün. Tahminler başlangıç paketini seçmek için yararlıdır; paketin gerçekten yeterli olup olmadığını ölçümler belirler.

### RAM bütçesi hesaplayıcısı {#ram-budget-estimator}

Ziyaretçi sayısından tahmin yürütmek yerine varsayımları görünür kılmak için bu hesaplayıcıyı kullanın. Yalnızca RAM paketini tahmin eder; CPU, depolama ve G/Ç ayrıca doğrulanmalıdır. Kendi ölçümlerinizi girin; örnek değerler aşağıdaki hesapla aynıdır ve evrensel varsayılanlar değildir.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="ram-budget-estimator-form">
  <div class="mb-6">
    <label for="ram-baseline" class="form-label">Temel işletim sistemi + web servisleri, MB</label>
    <input id="ram-baseline" class="form-input" type="number" min="0" step="1" placeholder="450" required>
  </div>
  <div class="mb-6">
    <label for="ram-database" class="form-label">Veritabanı çalışma belleği, MB</label>
    <input id="ram-database" class="form-input" type="number" min="0" step="1" placeholder="500" required>
  </div>
  <div class="mb-6">
    <label for="ram-workers" class="form-label">Eşzamanlı uygulama işçi süreçleri</label>
    <input id="ram-workers" class="form-input" type="number" min="0" step="1" placeholder="6" required>
  </div>
  <div class="mb-6">
    <label for="ram-worker-mb" class="form-label">Süreç başına ortalama bellek, MB</label>
    <input id="ram-worker-mb" class="form-input" type="number" min="0" step="1" placeholder="120" required>
  </div>
  <div class="mb-6">
    <label for="ram-background" class="form-label">Panel, önbellek ve arka plan görevleri, MB</label>
    <input id="ram-background" class="form-input" type="number" min="0" step="1" placeholder="300" required>
  </div>
  <div class="mb-6">
    <label for="ram-headroom" class="form-label">Güvenli kapasite payı, %</label>
    <input id="ram-headroom" class="form-input" type="number" min="0" max="100" step="1" value="25" required>
  </div>
  <button class="btn btn-primary" type="submit">RAM paketini hesaplayın</button>
</form>
<p id="ram-budget-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Ölçümlerinizi girin ve bütçeyi hesaplayın.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("ram-budget-estimator-form");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function number(id) {
      var value = Number(document.getElementById(id).value);
      return Number.isFinite(value) && value >= 0 ? value : 0;
    }
    var baseline = number("ram-baseline");
    var database = number("ram-database");
    var workers = number("ram-workers");
    var workerMb = number("ram-worker-mb");
    var background = number("ram-background");
    var headroom = number("ram-headroom");
    var subtotal = baseline + database + (workers * workerMb) + background;
    var required = subtotal * (1 + headroom / 100);
    var requiredGb = Math.round((required / 1024) * 10) / 10;
    var tier;
    if (required <= 1024) tier = "1 GB RAM";
    else if (required <= 2048) tier = "2 GB RAM";
    else if (required <= 4096) tier = "4 GB RAM";
    else if (required <= 8192) tier = "8 GB RAM";
    else tier = "8 GB RAM üzeri veya bileşenleri ayrılmış mimari";
    document.getElementById("ram-budget-result").textContent =
      "Birlikte çalışan bileşenlerin tahmini bütçesi: kapasite payı dahil yaklaşık " + requiredGb + " GB. Yalnızca RAM'e göre başlangıç paketi: " + tier +
      ". Siparişten önce gerçek süreç belleğini ve CPU ihtiyacını doğrulayın.";
  });
});
</script>

Hesap örneği: temel servisler için 450 MB + veritabanı için 500 MB + 6 süreç × 120 MB + panel/önbellek/arka plan görevleri için 300 MB = kapasite payı öncesi 1,970 MB. %25 payla bütçe yaklaşık 2.4 GB olur. Bu varsayımlarla 2 GB VPS fazla dardır; 4 GB daha güvenli başlangıç paketidir.

PHP-FPM veya benzeri süreçleri ölçerken ham RSS değerlerinin, süreçler arasında paylaşılan bellek sayfalarını ve kütüphaneleri birden fazla sayabileceğini unutmayın. Süreç ölçümlerini kusursuz biçimde toplanabilir hesaplar olarak değil, bulgu olarak değerlendirin.

### CPU bütçesi {#cpu-budget}

CPU ihtiyacı aynı anda ne kadar iş yapılacağına bağlıdır. Önbellekten sunulan statik dosyalar az maliyetli olabilir. Uygulama kodu çalıştıran, veritabanı sorgulayan, sayfa oluşturan, görsel boyutlandıran, içe aktarma yapan veya API işlemleri yürüten dinamik istekler çok daha fazla CPU tüketebilir.

Şu göstergeleri arayın:

- gerçek kullanıcı trafiği sırasında sürekli CPU doygunluğu;
- CPU meşgulken uzun uygulama istek süreleri;
- birkaç maliyetli dinamik isteğin aynı anda gelmesi;
- cron, yedekleme veya içe aktarma görevlerinin kullanıcı trafiğiyle çakışması;
- verimsiz indeksler veya aşırı işlem nedeniyle CPU tüketen veritabanı sorguları.

Kısa CPU sıçraması kendiliğinden yükseltme nedeni değildir. Gerçek işleri geciktiren sürekli doygunluk daha güçlü bir bulgudur.

Pratik bir eşzamanlılık tahmini:

**etkin dinamik istekler ≈ saniyedeki dinamik istekler × istek süresi**

Örnek: saniyede 6 önbelleksiz dinamik istek ve 0.8 saniyelik p95 süre, o anda yaklaşık 4.8 etkin isteğe karşılık gelir. Uygulama her etkin istek için bir süreç gerektiriyorsa yaklaşık beş meşgul süreç ve kuyruk/kapasite payı planlayın. Her istek 0.12 CPU-saniyesi tüketiyorsa saniyede 6 istek, pay eklenmeden saniyede yaklaşık 0.72 CPU-saniyesi iş demektir. Bu bir iş yükü tahminidir, evrensel vCPU garantisi değildir: CPU nesli, kaynak rekabeti ve sağlayıcı zamanlaması farklılık gösterir.

## Web sitesi iş yükü örnekleri {#website-workload-examples}

Kaynak sunucuya ulaşan iş miktarı iş yüküne göre değiştiğinden aynı trafik sayısı çok farklı VPS gereksinimleri doğurabilir.

| İş yükü | Tipik baskı | Kaynak seçimine etkisi |
|---|---|---|
| Çoğunlukla statik veya kapsamlı önbelleklenen site | düşük uygulama CPU'su, az süreç eşzamanlılığı, ağırlıkla dosya sunumu | küçük başlayın; yine de işletim sistemi, günlükler, yedekler ve beklenmeyen önbelleksiz istekler için bütçe ayırın |
| Küçük WordPress sitesi | PHP süreçleri, veritabanı okumaları, eklenti/cron etkinliği | RAM ve süreç payı genellikle ham aylık ziyaretlerden daha önemlidir |
| WooCommerce veya başka işlem odaklı site | önbelleksiz sepet, ödeme, hesap oturumları, zamanlanmış işlemler ve daha fazla veritabanı yazması | dinamik eşzamanlılığa, veritabanı gecikmesine ve yoğunluk çakışmasına öncelik verin; 1–2 GB'ı varsayılan canlı ortam hedefi saymayın |
| Birden fazla web sitesi | toplam PHP/uygulama süreçleri, veritabanları, cron görevleri ve çakışan yoğunluklar | toplam en yüksek ihtiyaca göre kaynak seçin; bir site diğerlerini kaynaksız bırakabiliyorsa yalıtımı değerlendirin |
| Arka plan süreçleri veya otomasyon ağırlıklı site | kuyruklar, içe/dışa aktarmalar, API çağrıları, görsel işleme, zamanlanmış görevler | kullanıcı isteklerinden ayrı CPU/RAM ayırın; ani yük oluşturan işler siteyi etkiliyorsa süreçleri ayırın |

Bunlar iş yükü örüntüleridir; platform garantisi değildir. Varsa gerçek ölçümleri kullanın.

## Paylaşımlı hosting sınırlarını VPS gereksinimlerine dönüştürün {#translate-shared-hosting-limits-into-vps-requirements}

Site zaten paylaşımlı hostingde çalışıyorsa kaynak seçimi için en yararlı bulgular hosting panelinde mevcut olabilir.

Şunları toplayın:

- CPU kullanımı ve CPU sınırı olayları;
- fiziksel bellek kullanımı;
- giriş süreci veya eşzamanlı istek sınırları;
- süreç sayısı;
- disk G/Ç ve IOPS baskısı;
- veritabanı boyutu ve büyümesi;
- depolama kullanımı;
- yalnızca aylık ziyaretler yerine saatlik trafik yoğunlukları;
- görünür olduğu yerde PHP işçi süreci veya uygulama süreci davranışı.

### Paylaşımlı hostingden VPS'e geçiş teşhisi {#shared-hosting-to-vps-diagnostic}

Paket seçmeden önce neyi incelemeniz gerektiğini hata örüntüsünden belirleyin. Araç, CloudLinux sınırını bilerek doğrudan vCPU veya RAM'e dönüştürmez.

CloudLinux kullanan cPanel hostinginde tek anlık ölçüm yerine Kaynak Kullanımı geçmişiyle başlayın. Tekrarlayan sınır aşımlarını ve saatlerini kaydedip trafik, cron, yedekleme, içe aktarma ve yönetim etkinliğiyle karşılaştırın.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="shared-hosting-diagnostic">
  <div class="mb-6">
    <label for="diag-evidence" class="form-label">Bulgularınızın niteliği</label>
    <select id="diag-evidence" class="form-input">
      <option value="measured">Panel geçmişi / ölçülmüş metrikler</option>
      <option value="partial">Bazı ölçülmüş metrikler</option>
      <option value="traffic">Yalnızca ziyaretçi sayısı veya izlenimler</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="diag-memory" class="form-label">Bellek sınırı aşımları / PMEM olayları</label>
    <select id="diag-memory" class="form-input"><option value="0">Yok</option><option value="1">Ara sıra</option><option value="2">Tekrarlıyor</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-cpu" class="form-label">CPU sınırı olayları</label>
    <select id="diag-cpu" class="form-input"><option value="0">Yok</option><option value="1">Ara sıra</option><option value="2">Tekrarlıyor</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-ep" class="form-label">Giriş süreci / işçi süreci doygunluğu</label>
    <select id="diag-ep" class="form-input"><option value="0">Yok</option><option value="1">Ara sıra</option><option value="2">Tekrarlıyor</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-nproc" class="form-label">Süreç sayısı / NPROC doygunluğu</label>
    <select id="diag-nproc" class="form-input"><option value="0">Yok</option><option value="1">Ara sıra</option><option value="2">Tekrarlıyor</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-io" class="form-label">G/Ç / IOPS baskısı</label>
    <select id="diag-io" class="form-input"><option value="0">Yok</option><option value="1">Ara sıra</option><option value="2">Tekrarlıyor</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Darboğazı değerlendirin</button>
</form>
<p id="shared-hosting-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Gerçekten gözlemlediğiniz göstergeleri seçin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("shared-hosting-diagnostic");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function value(id) { return Number(document.getElementById(id).value); }
    var memory = value("diag-memory");
    var cpu = value("diag-cpu");
    var ep = value("diag-ep");
    var nproc = value("diag-nproc");
    var io = value("diag-io");
    var evidence = document.getElementById("diag-evidence").value;
    var confidence = evidence === "measured" ? "Yüksek" : (evidence === "partial" ? "Orta" : "Düşük");
    var repeated = [memory, cpu, ep, nproc, io].filter(function (v) { return v === 2; }).length;
    var findings = [];
    if (memory >= 1) findings.push("bellek baskısı: süreç belleğini, veritabanının etkin veri kümesini, swap/OOM durumunu ve arka plan görevlerini kontrol edin");
    if (cpu >= 1) findings.push("CPU baskısı: vCPU eklemeden önce dinamik istekleri ve veritabanı işlemlerini profilleyin");
    if (ep >= 1) findings.push("süreç/eşzamanlılık baskısı: istek süresini azaltın ve önbelleksiz eşzamanlılığı ölçün");
    if (nproc >= 1) findings.push("süreç sayısı baskısı: kapasite satın almadan önce kontrolsüz veya aşırı PHP, cron ve arka plan süreçlerini bulun");
    if (io >= 1) findings.push("depolama baskısı: veritabanı G/Ç işlemlerini, yedekleri, günlükleri ve içe aktarmaları inceleyin; yalnızca RAM artırmak çözmeyebilir");
    var decision;
    if (findings.length === 0) decision = "Güçlü bir kapasite yetersizliği göstergesi yok. Ölçümler gerçek bir sınır gösterene kadar mevcut pakette kalın veya önce optimizasyon yapın.";
    else if (repeated >= 2) decision = "ÖLÇÜMLERE GÖRE GEÇİŞ / KAYNAK SEÇİMİ: belirgin yazılım verimsizlikleri giderildikten sonra birden fazla tekrarlayan sınır, VPS kaynak değerlendirmesini gerekçelendirir.";
    else decision = "ÖNCE OPTİMİZASYON, SONRA YENİDEN KONTROL: olası bir darboğaz var; ancak tek hosting sınırı doğrudan VPS teknik özelliğine çevrilemez.";
    document.getElementById("shared-hosting-result").textContent =
      decision + " Güven düzeyi: " + confidence + ". " + (findings.length ? findings.join("; ") + "." : "");
  });
});
</script>

Paylaşımlı hosting sınırını doğrudan VPS teknik özelliğine kopyalamayın. CloudLinux CPU yüzdesi, giriş süreci sınırı veya bellek üst sınırı mevcut hosting ortamını tanımlar; darboğaza dair bulgudur, bire bir VPS dönüşümü değildir.

Bunun yerine örüntüyü kullanın:

**CPU normalken tekrarlayan bellek sınırı olayları:** vCPU eklemeden önce süreç belleğini, veritabanı belleğini ve arka plan görevlerini inceleyin.

**Gerçek dinamik işlemlerde tekrarlayan CPU sınırı olayları:** uygulama ve veritabanını profilleyin; iş gerçekten gerekliyse ek CPU'yu değerlendirin.

**Giriş süreci veya işçi süreci doygunluğu:** dinamik eşzamanlılığı ve istek süresini ölçün. Daha hızlı istekler, daha büyük sunucu olmadan kuyruğu çözebilir.

**G/Ç baskısı:** RAM artırmanın çözeceğini varsaymadan önce yedekleri, günlükleri, veritabanı etkinliğini, içe aktarmaları veya depolama yoğun eklentileri belirleyin.

Bu, gerçek kapasite sorununu tek verimsiz bileşenin tetikleyebileceği hosting paketi sınırından ayırır.

<p class="vps-table-scroll-hint">Tüm sütunları görmek için tabloyu yana kaydırın.</p>

{{< table-scroll label="Kaynak darboğazları ve çözüm seçenekleri" >}}

| Belirti | Doğrulayın | Önce optimize edin | Ne zaman kaynak artırmalı? |
|---|---|---|---|
| Bellek sınırı aşımları, swap veya OOM | süreç belleği, veritabanının etkin veri kümesi, eşzamanlı süreçler | sızıntılar, büyük süreçler, önbellek/veritabanı ayarları | optimize edilmiş yük hâlâ RAM'i tüketiyorsa |
| CPU kısıtlaması | sürekli CPU yükü ve istek/veritabanı süreleri | yavaş kod, önbelleksiz işler, maliyetli sorgular | gerekli işler hâlâ CPU ile sınırlıysa |
| EP/süreç kuyruğu | dinamik eşzamanlılık ve istek süresi | önbellek, yavaş uç noktalar, süreç ayarları | istek maliyeti düşürüldükten sonra kuyruk sürüyorsa |
| G/Ç beklemesi / IOPS sınırı aşımları | veritabanı, günlükler, yedekler, içe aktarmalar | zamanlama, indeksler, günlük/yedek davranışı | normal yükte depolama yolu darboğaz olmaya devam ediyorsa |

{{< /table-scroll >}}



## VPS mi, web sitesi optimizasyonu mu? {#vps-or-website-optimization}

Belirgin uygulama sorunları giderildikten sonra gerçek iş yükü bir kaynağı tekrar tekrar tüketiyorsa daha büyük VPS gerekçelidir.

Baskı şunlardan geliyorsa önce optimizasyon yapın:

- tek yavaş eklenti veya uzantı;
- indekssiz veya sorunlu veritabanı sorgusu;
- çalışmayan sayfa veya nesne önbelleği;
- kötüye kullanım yapan botlar;
- kontrolsüz cron görevleri;
- aşırı büyük görsel işleme işleri;
- yoğun trafik saatine planlanmış yedekleme veya kötü amaçlı yazılım taramaları;
- bellek sızıntıları;
- aşırı günlük kaydı.

Ölçümler optimize edilmiş iş yükünün hâlâ ek kapasite gerektirdiğini gösteriyorsa sunucu kaynaklarını artırın.

Bu ayrım maliyet açısından önemlidir. Verimsiz kodu paylaşımlı hostingden daha büyük VPS'e taşımak, darboğazı ortadan kaldırmadan geçici olarak gizleyebilir.

## PHP ve uygulama işçi süreçlerini eşzamanlılığa göre boyutlandırın {#size-php-and-application-workers-from-concurrency}

Sunucular istekleri eşzamanlı karşıladığı için aylık ziyaretler zayıf bir kaynak seçimi verisidir.

Dinamik PHP yüklerinde her etkin süreç, isteği işlerken bellek ve CPU tüketir. Bu nedenle süreç kapasitesi hem süreç başına ortalama belleğe hem isteklerin ne kadar süre meşgul kaldığına bağlıdır.

Basitleştirilmiş RAM kontrolü:

**işçi süreç RAM bütçesi = temel servislerden sonra kullanılabilir RAM × süreçlere güvenle ayrılabilen oran**

Ardından bütçeyi ölçülen süreç belleğiyle karşılaştırın. Veritabanı, önbellek veya işletim sistemine bellek bırakmayacaksa teorik azami süreç sayısını yapılandırmayın.

Önbellekleme bu hesabı değiştirir. Anonim kullanıcı için önbellekli sayfa PHP'yi tamamen atlayabilir; ödeme, oturum açmış kullanıcılar, wp-admin, API'ler ve kişiselleştirilmiş sayfalar uygulamaya ulaşmaya devam eder.

WordPress'e özgü davranışlar için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberine bakın. İşlem odaklı yükler için [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) rehberini inceleyin.

## Sunucu boyutunu veritabanı ihtiyacı belirleyebilir {#database-demand-can-set-the-server-size}

Temel sorun veritabanı işlemleri olduğu halde site CPU ile sınırlı görünebilir.

Şunları kontrol edin:

- yavaş sorgu örüntüleri;
- veritabanının etkin veri kümesi boyutu;
- sorgu eşzamanlılığı;
- eksik indeksler;
- büyük otomatik yüklenen veri kümeleri veya eşdeğer uygulama meta verileri;
- maliyetli arama, filtreleme veya raporlama işlemleri;
- içe aktarma ve bakım görevleri;
- depolama gecikmesi.

Veritabanı gerçekten daha büyük etkin veri kümesi gerektiriyorsa RAM artırmak yardımcı olabilir; ancak verimsiz sorguları düzeltmez. CPU artırmak işlem hacmini yükseltebilir; aynı zamanda daha fazla maliyetli sorgunun eşzamanlı rekabet etmesine de izin verebilir.

## Ortalama trafik yerine yoğun saatleri planlayın {#plan-for-peak-traffic-not-average-traffic}

Ortalamaya göre kaynak seçimi, kullanıcıların gerçekten hata yaşadığı dönemleri gizler.

Gerçekçi en yoğun aralığı belirleyin: kampanya başlangıçları, indirimler, bülten gönderimleri, ürün lansmanları, zamanlanmış içe aktarmalar, yedekler veya cron yoğunlukları. Bu aralıkta hangi isteklerin dinamik kalacağını, hangilerinin sayfa önbelleği veya CDN ile karşılanabileceğini tahmin edin.

Şunların birleşimi için pay bırakın:

- normal kullanıcı trafiği;
- yoğun dinamik trafik;
- yönetim etkinliği;
- zamanlanmış görevler;
- dağıtımlar ve önbelleğin doldurulması;
- izleme ve yedekleme süreçleri.

CDN, statik içerik sunumunu ve bazı kaynak sunucu isteklerini azaltabilir. VPS'e ulaşan dinamik uygulama veya veritabanı işlerini ortadan kaldırmaz.

Yoğunluk örneği: site saniyede 20 istek alıyorsa ve %90'ı önbellek/CDN'den karşılanıyorsa kaynak sunucu yaklaşık 2 dinamik istek/s görür. Toplam trafiği aynı önbellek oranıyla 40 istek/s'ye çıkaran kampanya, uygulamaya yaklaşık 4 dinamik istek/s gönderir. 0.8 saniyelik p95 sürede bu; yönetim işleri veya ödeme/API sıçramaları eklenmeden yaklaşık 3.2 eşzamanlı etkin dinamik istek demektir.

## Depolama boyutlandırması {#storage-sizing}

Disk kapasitesi yalnızca mevcut web sitesi dizini değildir.

Şunları dahil edin:

- web sitesi dosyaları;
- veritabanı;
- yüklenen medya;
- günlükler;
- geçici dosyalar;
- paket ve uygulama önbellekleri;
- yerel tutuluyorsa test ortamı kopyaları;
- geçici olarak VPS'te oluşturuluyorsa yedek dosyaları;
- beklenen büyüme.

Dosya sistemini sınırına kadar doldurmayın. Veritabanları, güncellemeler, günlükler ve yedekleme işlemleri çalışma alanı gerektirir.

Pratik bir kapasite bütçesi:

**gerekli disk = mevcut dosyalar + veritabanı + geçici işlem alanı + yerel yedek hazırlama alanı + beklenen büyüme + boş çalışma payı**

Örnek: kullanılan 18 GB + taşıma/güncelleme için 8 GB geçici alan + yerel yedek hazırlama için 18 GB + beklenen 6 GB büyüme, güvenlik payı eklenmeden 40 GB diski aşar. Bu senaryoda 80 GB paket daha güvenli başlangıçtır. Kapasite, IOPS ve depolama gecikmesinden ayrıdır: büyük disk yavaş veritabanını kendiliğinden hızlandırmaz.

## Bant genişliği ve aylık veri aktarımı hesabı {#bandwidth-and-monthly-transfer-sizing}

Aylık veri aktarımı CPU, RAM ve port hızından farklıdır. Sunucunun işlem kapasitesi bol olsa bile büyük dosyaları veya önbelleksiz medyayı doğrudan sunması aktarım kotasını aşabilir.

Kaba tahmin:

**aylık kaynak sunucu aktarımı ≈ istek başına VPS'ten gönderilen ortalama bayt × aylık kaynak sunucu isteği + yedekler/dışa aktarmalar/diğer çıkış trafiği**

Daha yararlı tahmin için önbelleğe alınabilir ve dinamik trafiği ayırın:

**kaynak sunucu aktarımı ≈ talep edilen toplam bayt × (1 - CDN/önbelleğin karşıladığı oran) + önbelleksiz dinamik yanıtlar + web dışı çıkış trafiği**

Örnek: kullanıcılar ayda 2 TB dosya/sayfa talep ediyorsa ve CDN bu baytların %80'ini kaynak sunucuya dönmeden sunuyorsa VPS, bu önbelleklenebilir trafiğin yaklaşık 400 GB'ını iletebilir. Dinamik sayfalar, API yanıtları, yedekler, dışa aktarmalar ve önbellek kaçırmaları buna eklenir.

CDN'in kaynak sunucu aktarımını sıfırladığını varsaymayın. Oturum açılmış sayfalar, ödeme, API'ler, önbellek kaçırmaları, temizleme işlemleri, büyük indirmeler ve kaynak sunucudan CDN'e önbellek doldurma hâlâ aktarım tüketebilir. Ayrıca **aylık veri aktarım kotasını** **ağ port hızından** ayrı tutun: hızlı port potansiyel aktarım hızını, kota ise fatura döneminde gönderilebilen veri miktarını tanımlar.

## Birden fazla web sitesi hesabı değiştirir {#multiple-websites-change-the-calculation}

Tek VPS'teki birkaç site aynı CPU, RAM, depolama ve süreç kapasitesini paylaşır. Her biri tek başına küçük olsa bile yoğunlukları çakışabilir.

Sunucuyu toplam iş yüküne göre boyutlandırın ve bir sitenin arka plan görevinin diğerlerini kaynaksız bırakmayacağı kadar pay ayırın. Yalıtım, arıza etkisi veya kaynak rekabeti önem kazandığında iş yüklerini ayırmak, tek sunucuyu sürekli büyütmekten daha yararlı olabilir.

Çoklu site kararı için [birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) rehberine bakın.

## Kontrol paneli ve e-posta yükünü bütçeye dahil edin {#control-panel-and-mail-overhead-belong-in-the-budget}

Kontrol paneli alan adı, SSL, veritabanı, PHP sürümü ve hesap yönetimini kolaylaştırır; ancak kendi servislerini de çalıştırır. Kaynakları yalnızca siteye göre seçmek yerine panel için de bellek ve depolama ayırın.

E-posta servisleri sürekli kaynak kullanan ayrı bir katman ekleyebilir: SMTP, IMAP/POP, spam filtreleme, antivirüs taraması, kuyruklar, günlükler ve posta kutusu depolaması. VPS hem siteyi hem e-postayı barındıracaksa e-postayı bedelsiz kaynak gibi görmeyin; RAM, CPU, depolama ve yedek bütçesine ekleyin.

Küçük bir sitede e-postayı yönetilen e-posta sağlayıcısına taşımak sunucu yükünü ve işletim riskini azaltabilir. E-posta VPS'te kalacaksa DNS kayıtları ve sağlayıcı/IP kısıtları gibi teslimat gereksinimlerini ayrıca doğrulayın; daha büyük VPS, gönderici itibarını çözmez.

Panel üzerinden yönetimi tercih ediyorsanız [kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) rehberindeki avantaj ve kısıtları karşılaştırın.

## Tekrarlanabilir VPS kaynak seçimi süreci {#a-repeatable-vps-sizing-workflow}

1. **Mevcut iş yükünü ölçün.** CPU, bellek, dinamik eşzamanlılık, veritabanı davranışı, depolama ve yoğun dönemleri kaydedin.
2. **Darboğazı belirleyin.** CPU, RAM, süreç, veritabanı, G/Ç ve yazılım sınırı sorunlarını ayırın.
3. **Belirgin verimsizlikleri giderin.** Kapasite almadan önce önbelleği, kontrolsüz görevleri, sorunlu sorguları ve kötüye kullanım trafiğini düzeltin.
4. **Kaynak bütçesini oluşturun.** Temel servisler, veritabanı, uygulama süreçleri, panel ve arka plan işleri için RAM ayırın.
5. **Pay bırakan başlangıç paketi seçin.** Hem sıfır payla boyutlandırmadan hem varsayıma dayalı aşırı kaynak alımından kaçının.
6. **Gerçekçi yoğunluğu yeniden oluşturun.** Yapılandırmayı yalnızca boşta duran ana sayfada değil, gerçek kullanımı temsil eden dinamik yük altında doğrulayın.
7. **Taşıma sonrasında izleyin.** İlk tahmini kalıcı saymak yerine ölçümlere göre ayarlayın; canlı ortamın temel düzeni için [VPS izleme]({{< relref "vps-monitoring.md" >}}) rehberini kullanın.

Hedef ortamın kaynakları belirlendiğinde envanter, özel test, son veri eşitlemesi, DNS geçişi ve geri dönüş yolunu planlamak için [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberini kullanın.

## Ölçümlere dayalı öneri {#evidence-based-recommendation}

Yararlı VPS önerisi hem yapılandırmayı hem gerekçesini belirtmelidir.

Örneğin:

Kurumsal site veritabanı kullanan CMS çalıştırıyorsa, kayda değer önbelleksiz PHP etkinliği varsa, kontrol paneli istiyorsa ve işletim payı gerektiriyorsa **2 vCPU / 4 GB RAM / 80 GB** makul başlangıç olabilir. Bu, sunucunun belirli aylık ziyaretçi sayısını desteklediği garantisi değildir.

Tek girdi ziyaretçi sayısı olduğunda güven düzeyi daha düşük olmalıdır. CPU geçmişi, bellek baskısı, eşzamanlı dinamik istekler, süreç belleği, veritabanı davranışı ve depolama artışı bilindiğinde güven yükselir.

Basit bir güven düzeyi etiketi kullanın:

- **Düşük güven:** yalnızca ziyaretçi sayısı, CMS adı ve yaklaşık depolama.
- **Orta güven:** iş yükü türü ve yoğunluk örüntüsünün yanında bazı gerçek CPU/RAM geçmişi.
- **Yüksek güven:** zaman içindeki CPU/RAM/G/Ç ölçümleri, önbelleksiz eşzamanlılık, süreç belleği, istek süresi, veritabanı davranışı ve depolama artışı.

Daha yüksek güven etiketi varsayımların daha sağlam olduğunu gösterir; gelecekteki trafiği garanti etmez.

## Sonucu VPS paketiyle eşleştirin {#match-the-result-to-a-vps}

RAM tahmini, CPU bulguları, depolama bütçesi ve yoğunluk davranışını birlikte kullanın. Bu VDSina Standard yapılandırmaları sonucu eşlemek için örnektir; siparişten önce güncel sağlayıcı koşullarını doğrulayın.

<p class="vps-table-scroll-hint">Tüm sütunları görmek için tabloyu yana kaydırın.</p>

{{< table-scroll label="VPS yapılandırmalarının karşılaştırması" >}}

| Yapılandırma | Uygun başlangıç kullanımı | Kaçının / yeniden değerlendirin | Temel doğrulama | İşlem |
|---|---|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/gün, 1 TB/ay | test sitesi, çok hafif önbellekli site, asgari servisler | panel + veritabanı + birkaç dinamik süreç, canlı mağaza | RAM payı ve disk | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel paketi inceleyin</a> |
| 1 vCPU / 2 GB / 40 GB — $0.50/gün, 32 TB/ay | kontrollü dinamik yükü olan hafif küçük site veya CMS | sürekli CPU yükü, birkaç etkin site, ağır panel/e-posta ortamı | süreç belleği, veritabanı belleği, depolama artışı | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel paketi inceleyin</a> |
| 2 vCPU / 4 GB / 80 GB — $0.67/gün, 32 TB/ay | dinamik kurumsal CMS, orta yoğunlukta önbelleksiz PHP, panel payı | ağır WooCommerce, büyük içe aktarmalar, yüksek veritabanı baskısı, çakışan çoklu site yoğunlukları | CPU doygunluğu, veritabanı gecikmesi, yoğunluk çakışması | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel paketi inceleyin</a> |
| 4 vCPU / 8 GB / 160 GB — $1.34/gün, 32 TB/ay | daha ağır dinamik yük, büyük veritabanı, birkaç etkin site | katı yüksek erişilebilirlik gereksinimi, çok yoğun yazma yükü, bağımsız ölçeklendirme ihtiyacı | tek VPS'in hâlâ doğru mimari olup olmadığı | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel paketi inceleyin</a> |

{{< /table-scroll >}}

Site açılabiliyor diye 1 GB veya 2 GB paket varsayılan canlı ortam önerisi sayılmamalıdır. E-ticaret, büyük veritabanları, birkaç dinamik site, e-posta servisleri ve kontrol panelleri kapasite payını hızla tüketebilir.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">VPS'inizi seçin</a>
</p>

## VPS satın almadan önce {#before-buying-the-vps}

Tek başına kaynak hesabının yanıtlamadığı altyapı koşullarını kontrol edin: veri aktarım kotası, depolama türü ve kapasitesi, IP koşulları, yedek politikası, yükseltme yolu, yönetim kapsamı, panel lisansı ve güncel faturalandırma koşulları. CPU/RAM hesabı en iyi ağ yolunu belirlemediğinden bölgeyi [VPS sunucu konumu seçimi]({{< relref "how-to-choose-vps-location.md" >}}) rehberiyle ayrıca seçin.

Site hâlâ paylaşımlı hostingdeyse taşımadan önce işletim değişikliğini [VPS ve paylaşımlı hosting karşılaştırmasında]({{< relref "vps-vs-shared-hosting.md" >}}) değerlendirin.

## Teknik kaynaklar {#technical-references}

- cPanel: sunucu donanım gereksinimleri
- cPanel: ne kadar RAM, CPU ve disk ekleneceğini belirleme
- VDSina Standard VPS yapılandırmaları

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS teklifini inceleyin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır. İş ortaklığı bağlantıları sponsored olarak işaretlidir. Sağlayıcının fiyatları, veri aktarım koşulları ve diğer ticari şartları değişebilir; siparişten önce sağlayıcı sitesinde doğrulayın.</small></p>

## Sık sorulan sorular {#faq}

### Web sitesi VPS'i ne kadar RAM gerektirir? {#how-much-ram-does-a-website-vps-need}

Güvenilir evrensel miktar yoktur. Hafif ve önbellekli site az bellek kullanabilir; veritabanı, panel ve eşzamanlı uygulama süreçleri olan dinamik CMS çok daha fazlasını gerektirebilir. RAM'i birlikte çalışması gereken süreçlere göre hesaplayıp pay bırakın.

### Web sitesi VPS'i için 2 GB RAM yeterli mi? {#is-2-gb-ram-enough-for-a-website-vps}

Küçük, hafif iş yükü için yeterli olabilir. Kontrol paneli, veritabanı, birkaç PHP süreci, arka plan görevleri veya birden fazla site birlikte çalışacaksa sınırlayıcı hale gelir. Yalnızca RAM rakamına güvenmek yerine bellek baskısını ölçün.

### 4 GB VPS paketi neye uygundur? {#what-does-a-4-gb-vps-tier-fit}

4 GB VPS; Linux, veritabanı, uygulama/PHP süreçleri ve önbelleğe daha fazla alan bıraktığı için birçok kurumsal CMS yükünde pratik başlangıçtır. Kesin uygunluk dinamik eşzamanlılığa, veritabanı ihtiyacına, arka plan işlerine ve panel yüküne bağlıdır. WordPress'e özgü karar için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberini kullanın.

### VPS kaç ziyaretçiyi kaldırır? {#how-many-visitors-can-a-vps-handle}

Yalnızca ziyaretçi sayısı bu soruyu yanıtlayamaz. Önbellek isabet oranı, eşzamanlı istekler, uygulama çalışma süresi, veritabanı işleri ve arka plan görevleri; benzer trafikli iki site arasında kapasiteyi kat kat değiştirebilir.

### Önce RAM mi CPU mu eklemeliyim? {#should-i-add-ram-or-cpu-first}

Ölçümlerin sınırlı olduğunu gösterdiği kaynağı ekleyin. Bellek baskısı, swap etkinliği veya OOM olayları RAM'i ya da bellek optimizasyonunu işaret eder. Gerekli ve optimize edilmiş iş sırasında sürekli CPU doygunluğu CPU'yu işaret eder. Veritabanı ve G/Ç darboğazları ayrıca teşhis edilmelidir.

### CDN, VPS gereksinimlerini azaltır mı? {#does-a-cdn-reduce-vps-requirements}

Statik dosya sunumunu ve önbelleğe alınabilir kaynak sunucu isteklerini azaltabilir. Kaynak sunucuya ulaşan dinamik uygulama istekleri ve veritabanı işleri VPS kaynaklarını tüketmeye devam eder.

### Ortalama trafiğe mi yoğun trafiğe mi göre kaynak seçmeliyim? {#should-i-size-for-average-or-peak-traffic}

İşletim payı bırakarak gerçekçi yoğunluğa göre seçin. Ortalama trafik; eşzamanlılık, zamanlanmış görevler ve dinamik isteklerin çakıştığı kısa dönemleri gizleyebilir.
