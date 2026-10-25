---
title: "VPS izleme"
description: "Harici erişilebilirlik kontrolleri, CPU/RAM/disk/ağ metrikleri, hizmet sağlığı, günlükler ve müdahaleye yönelik uyarılarla VPS izleme. Araçlar, eşikler ve uygulanabilir kontrol listesi."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-izleme"
---

VPS izleme, «sunucu açık mı?» sorusundan fazlasını yanıtlamalıdır. Canlı kullanımda temel izleme; **harici erişilebilirlik kontrolleri, geçmiş sunucu metrikleri, hizmet ve uygulama sağlığı, günlükler, müdahaleye yönelik uyarılar ve belirli bir müdahale sorumlusu** gerektirir.

Nginx bozukken, veritabanı takılmışken, disk doluyken veya TLS sertifikasının süresi dolmak üzereyken VPS ping'e yanıt verebilir. Bu yüzden izleme hem sunucuyu hem de kullanıcının gördüğü web sitesini kapsamalıdır.

Genel sunucu seçimi için [Web sitesi için VPS]({{< relref "_index.md" >}}) sayfasına bakın.

[Kısa yanıt](#quick-answer) · [Kontrol aracı](#vps-monitoring-baseline-checker) · [Sunucu metrikleri](#monitor-cpu-memory-disk-and-network) · [Uygulama sağlığı](#monitor-services-and-application-health) · [Uyarılar](#build-actionable-alerts) · [Kapasite](#use-trends-for-capacity-planning) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

Uygulanabilir bir VPS izleme sistemi beş katmandan oluşur:

| Katman | Ne gösterir? | Yakaladığı tipik sorun |
|---|---|---|
| **Harici erişilebilirlik** | kullanıcıların VPS dışından siteye ulaşıp ulaşamadığı | VPS, ağ veya siteye erişilememesi |
| **Sunucu metrikleri** | CPU, RAM, swap, disk, inode, G/Ç ve ağ eğilimleri | bellek sızıntısı, disk dolması, sürekli CPU baskısı |
| **Hizmet ve uygulama sağlığı** | web sunucusu, çalışma ortamı, veritabanı ve kritik uç noktaların gerçekten çalışıp çalışmadığı | sunucu çevrimiçiyken Nginx, PHP, veritabanı veya uygulama arızası |
| **Günlükler ve olaylar** | neyin değiştiği veya bozulduğu | 5xx artışı, OOM, başarısız işçi süreci, veritabanı hatası |
| **Uyarılar ve sorumluluk** | doğru kişinin bilgilendirilip müdahale edip edemediği | sessiz kesinti veya takip edilmeyen gösterge paneli |

Tek erişilebilirlik izleyicisini, izlemesi gereken VPS üzerinde çalıştırmayın. VPS veya ağ yolu tamamen arızalanırsa izleyici de onunla birlikte kaybolabilir.

## VPS temel izleme kontrol aracı {#vps-monitoring-baseline-checker}

İzlenmeyen noktaları bulmak için bu aracı kullanın. Araç kesintisizlik garantisi vermez.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">Ana iş yükü</label>
    <select id="mon-workload" class="form-input">
      <option value="static">Statik / basit web sitesi</option>
      <option value="cms">WordPress / CMS</option>
      <option value="transactional">WooCommerce / işlem yapan site</option>
      <option value="multi">Birden fazla web sitesi / karma portföy</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">Bu VPS'nin dışından HTTP(S) erişilebilirlik kontrolü var mı?</label>
    <select id="mon-external" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">Geçmiş CPU, RAM, disk ve ağ metrikleri saklanıyor mu?</label>
    <select id="mon-metrics" class="form-input"><option value="no">Hayır / yalnızca gerektiğinde top veya htop</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">Disk kapasitesi, inode kullanımı ve depolama baskısı izleniyor mu?</label>
    <select id="mon-disk" class="form-input"><option value="no">Hayır / yalnızca boş GB</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">Kritik hizmet ve uygulama sağlık kontrolleri ayarlandı mı?</label>
    <select id="mon-app" class="form-input"><option value="no">Hayır / yalnızca ping</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">Gerektiğinde veritabanı, kuyruk, cron ve yedeklerin güncelliği izleniyor mu?</label>
    <select id="mon-jobs" class="form-input"><option value="no">Hayır / bilinmiyor</option><option value="yes">Evet</option><option value="na">Uygulanamaz</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">Otomatik uyarılarda uygun önem ve süre kuralları tanımlı mı?</label>
    <select id="mon-alerts" class="form-input"><option value="no">Hayır / yalnızca gösterge paneli</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">Bildirim yolu bu VPS arızalansa da çalışıyor mu?</label>
    <select id="mon-notify" class="form-input"><option value="no">Hayır / yalnızca aynı VPS</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">Belirli bir sorumlu ve ilk müdahale rehberi var mı?</label>
    <select id="mon-owner" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Temel izlemeyi kontrol edin</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Yalnızca gerçekten veri toplayan ve uyarı ileten izleme kontrollerini işaretleyin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-monitoring-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function yes(id) { return document.getElementById(id).value === "yes"; }
    var workload = document.getElementById("mon-workload").value;
    var external = yes("mon-external");
    var metrics = yes("mon-metrics");
    var disk = yes("mon-disk");
    var app = yes("mon-app");
    var jobsValue = document.getElementById("mon-jobs").value;
    var jobs = jobsValue === "yes" || jobsValue === "na";
    var alerts = yes("mon-alerts");
    var notify = yes("mon-notify");
    var owner = yes("mon-owner");

    var result;

    if (!external || !metrics || !app || !disk) {
      result = "GÖRÜNMEYEN SORUNLAR: izleme sistemi henüz bir veya daha fazla temel arıza türünü göremiyor. Bağımsız erişilebilirlik kontrolleri, geçmişi saklanan sunucu metrikleri, disk/inode görünürlüğü ve gerçek hizmet/uygulama sağlık kontrolleri ekleyin.";
    } else if (!alerts || !notify || !owner) {
      result = "UYARI VEYA SORUMLULUK EKSİK: veriler mevcut olabilir; ancak olay fark edilmeyebilir veya sorumlusu olmayabilir. Müdahale edilebilir uyarılar, bağımsız bildirim yolu ve sorumlusu belirli bir müdahale rehberi ekleyin.";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "TEMEL İZLEME: altyapı izleme mevcut, ancak bu iş yükünde uygulama görevleri, veritabanı veya yedeklerin güncelliği hâlâ izlenmiyor.";
    } else {
      result = "CANLI KULLANIM İÇİN TEMEL İZLEME: dışarıdan erişilebilirlik, geçmiş metrikler, hizmet sağlığı, uyarılar ve müdahale sorumluluğu mevcut. Eşikleri gerçek ölçümlere göre ayarlamaya devam edin; bu, kesintisizlik garantisi değildir.";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## Web sitesini VPS dışından izleyin {#monitor-the-website-from-outside-the-vps}

Sunucuda çalıştırılan bir komut Nginx'in çalıştığını gösterebilir. Ancak internetteki gerçek bir kullanıcının web sitesine ulaşabildiğini kanıtlayamaz.

Önemli ana makine adları için harici izleyici kullanın.

Yararlı kontroller şunlardır:

- HTTP ve HTTPS erişilebilirliği;
- beklenen durum kodu;
- yanıt süresi;
- anahtar kelime veya içerik kontrolü;
- DNS çözümlemesi;
- TLS sertifikasının durumu ve son kullanma tarihi;
- gerektiğinde TCP port kontrolleri.

Yanlış alarmlar önemliyse birini acil müdahaleye çağırmadan önce tekrarlanan başarısızlıklar veya birden fazla konumdan doğrulama şartı koyun.

Kendi sunucunuzda çalıştırılabilen Uptime Kuma gibi araçlar HTTP(S), anahtar kelime, TCP, ping ve DNS kontrolleri yapabilir. Ancak izleyiciyi canlı VPS'nin arıza alanının dışında konumlandırın.

Aynı VPS'yi, sağlayıcı ağını veya DNS arızasını paylaşan bir izleme sunucusu gösterge panelleri için yararlı olabilir; ancak bağımsız erişilebilirlik kontrolü değildir.

## Anlık tanılama, geçmişe dönük izleme değildir {#real-time-diagnostics-are-not-historical-monitoring}

Şu tür komutlar:

```bash
top
htop
free -h
df -h
ss -s
```

bir sorunu zaten araştırırken yararlıdır.

Ancak şunları göstermezler:

- 03:12'de ne olduğu;
- RAM kullanımının altı saat boyunca düzenli artıp artmadığı;
- yedekleme sırasında disk gecikmesinin yükselip yükselmediği;
- web sitesinin on dakika kapalı kalıp kalmadığı;
- sorunun haftadan haftaya kötüleşip kötüleşmediği.

Erişilebilirliği ve kapasiteyi etkileyen sinyallerin zaman serisi geçmişini saklayın.

Tek VPS için hafif bir izleme ajanı yeterli olabilir. Sunucu filosu, uzun saklama süresi veya özel gösterge panelleri için Prometheus + Node Exporter + Grafana yaygın bir mimaridir.

Prometheus Node Exporter; CPU, dosya sistemi ve ağ verileri dahil, Prometheus'un toplayabileceği sunucu ve çekirdek metriklerini sunar.

## CPU, bellek, disk ve ağı izleyin {#monitor-cpu-memory-disk-and-network}

### CPU {#cpu}

Her kısa yükselişte uyarı üretmeyin.

Şunları izleyin:

- sürekli CPU kullanımı;
- vCPU sayısına göre yük ortalaması;
- süreç başına CPU kullanımı;
- sanallaştırma katmanı sunuyorsa CPU steal süresi;
- aynı andaki uygulama ve istek gecikmesi.

Önbellek ısınırken veya cron görevi çalışırken kısa süreli %100 kullanım zararsız olabilir. Sürekli CPU doygunluğu ile artan gecikme ve kuyruklar, gerçek bir darboğaz için daha güçlü kanıttır.

### Bellek, swap ve OOM {#memory-swap-and-oom}

Linux, boş RAM'i sıklıkla dosya sistemi önbelleği için kullanır. Bu yüzden «RAM'in %90'ı kullanılıyor» ifadesi otomatik olarak arıza anlamına gelmez.

Şunları izleyin:

- kullanılabilir bellek;
- swap etkinliği;
- swap kullanımının artışı;
- OOM killer olayları;
- süreç belleğinin büyümesi;
- PHP ve uygulama işçi süreçlerinin belleği;
- veritabanı belleği.

Bellek sızıntısı öğlen normal görünüp gece süreci sonlandırabilir. Bunu ortaya çıkaran, geçmiş eğilim verileridir.

### Disk kapasitesi {#disk-capacity}

Veritabanları, günlükler veya paket güncellemeleri başarısız olacak noktaya gelmeden dosya sistemi kullanımını izleyin.

Başlangıç için örnek uyarı/kritik eşikleri **%80 / %90 doluluk** olabilir; ancak bunlar evrensel bir SLA değildir. Hızla büyüyen bir veritabanı çok daha erken müdahale gerektirebilir.

Şunların gerektirdiği boş çalışma alanını da izleyin:

- yedekler;
- veritabanı bakımı;
- paket güncellemeleri;
- yüklenen dosyalar;
- günlükler;
- hazırlık ve içe aktarma görevleri.

### Inode kullanımı {#inodes}

Diskte çok sayıda GB boş kalsa da dosya sisteminin inode'ları tükenebilir.

Buna şunlar yol açabilir:

- önbellek dizinleri;
- oturumlar;
- posta kuyrukları;
- çok büyük sayıda küçük dosya;
- kontrolsüz büyüyen geçici dosyalar.

Inode kullanımını diskteki GB miktarından ayrı izleyin.

### Disk G/Ç ve gecikme {#disk-io-and-latency}

Disk, kapasitesi dolmadan önce darboğaz haline gelebilir.

Şunları izleyin:

- G/Ç bekleme süresi;
- okuma ve yazma gecikmesi;
- sunuluyorsa kuyruk derinliği;
- veritabanı yanıt süresi;
- yedekleme ve içe aktarma zaman aralıkları.

Daha büyük disk kapasitesi, yavaş depolama G/Ç'sini otomatik olarak düzeltmez.

### Ağ {#network}

Toplam bant genişliğinden fazlasını takip edin:

- gelen ve giden veri aktarım hızı;
- ani trafik değişiklikleri;
- bağlantı hataları;
- ölçülebildiğinde paket kaybı ve gecikme;
- olağandışı giden trafik;
- ağ arayüzü hataları.

Ağ metrikleri, uygulama yavaşlığını sağlayıcı veya ağ yolu sorunlarından ayırmaya yardımcı olur.

## Hizmetleri ve uygulama sağlığını izleyin {#monitor-services-and-application-health}

Web sitesi bozukken VPS erişilebilir olabilir.

Şu önemli hizmetleri izleyin:

- Nginx/Apache;
- PHP-FPM;
- Node veya Python uygulama hizmeti;
- MySQL/MariaDB/PostgreSQL;
- kullanılıyorsa Redis;
- kuyruk işçi süreçleri;
- zamanlanmış görev hizmeti;
- iş açısından kritikse kontrol paneli.

systemd tabanlı Linux'ta `systemctl --failed` tanılama sırasında yararlıdır. Sürekli izleme ise gerekli hizmetler başarısız olduğunda veya tekrar tekrar yeniden başladığında uyarı vermelidir.

«Süreç mevcut» kontrolüyle yetinmeyin. Bir süreç çalışıyor görünüp geçerli isteklere yanıt veremeyebilir.

## HTTP 200 her zaman sağlıklı demek değildir {#http-200-is-not-always-healthy}

Uygulama şu durumlarda da HTTP 200 döndürebilir:

- bakım sayfası;
- şablon içinde gösterilen veritabanı hatası;
- boş veya yanlış içerik;
- bozuk oturum açma akışı;
- eski önbellek.

Kritik sitelerde amaca yetecek en dar kapsamlı kontrolü kullanın:

- beklenen anahtar kelime veya metin;
- sağlık kontrolü uç noktası;
- API yanıtı;
- kritik genel URL;
- yalnızca iş değeri karmaşıklığı haklı çıkarıyorsa yapay oturum açma veya işlem testi.

Güvenle veri değiştirmek için özel olarak tasarlanmadıkça yapay kontrollerin canlı verileri değiştirmesine izin vermeyin.

## TLS ve DNS'i izleyin {#monitor-tls-and-dns}

Sertifika veya DNS hatası nedeniyle web sitesi erişilemezken VPS sağlıklı olabilir.

Şunları takip edin:

- sertifika süresinin dolması;
- sertifika ile ana makine adı uyuşmazlığı;
- başarısız yenileme;
- DNS çözümlemesi;
- araç destekliyorsa yanlışlıkla yapılan kayıt değişiklikleri.

Yararlı bir örnek, sertifika dolmadan çok önce, örneğin **14 gün** kala uyarı vermek ve süre yaklaştıkça, örneğin **7 gün** kala önem düzeyini artırmaktır. Kesin aralık, yenilemenin ne kadar hızlı düzeltilebildiğine uygun olmalıdır.

## Veritabanını bir uygulama bağımlılığı olarak izleyin {#monitor-the-database-as-an-application-dependency}

Veritabanı kullanan sitelerde, veritabanının darboğaz mı yoksa arızalı bağımlılık mı olduğunu anlayacak kadar izleme yapın.

Motora ve iş yüküne göre yararlı sinyaller şunları içerir:

- hizmet erişilebilirliği;
- bağlantı sayısı;
- bağlantı hataları;
- sorgu gecikmesi;
- kilit ve kaynak çekişmesi belirtileri;
- yavaş sorgu etkinliği;
- bellek baskısı;
- depolama büyümesi;
- kullanılıyorsa çoğaltma ve yedekleme durumu.

Her veritabanı metriği için uyarı vermeyin. Kullanıcı etkisi veya bilinen bir arıza türüyle bağlantılı koşullarda uyarı üretin.

WordPress iş yükü davranışı için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}), işlem yapan mağaza iş yükü için [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) sayfasına bakın.

## Cron, kuyruklar ve arka plan görevlerini izleyin {#monitor-cron-queues-and-background-jobs}

Ana sayfanın sağlıklı görünmesi, arka plan işlerinin de sağlıklı olduğunu kanıtlamaz.

Uygulama için önemli görevleri takip edin:

- cron;
- kuyruk işçi süreçleri;
- zamanlanmış içe aktarmalar;
- webhook'lar;
- e-posta görevleri;
- WordPress WP-Cron ve sistem cron'u;
- WooCommerce Action Scheduler;
- abonelikler ve yenilemeler;
- stok eşitleme.

Yararlı sinyaller:

- son başarılı çalışma;
- kuyruk derinliği ve birikimi;
- başarısız görevler;
- bekleyen en eski görev;
- tekrarlanan yeniden denemeler;
- işçi sürecinin durması veya yeniden başlaması.

WooCommerce'te başarısız veya gecikmiş Action Scheduler kuyruğunun büyümesi, katalog sayfaları hâlâ açılıyor olsa da operasyon sorunu olabilir.

## Yedeklerin güncelliğini izleyin {#monitor-backup-freshness}

Yedekleme görevi kurtarma stratejisinin parçasıdır; ancak **yedeğin güncelliği bir izleme sinyalidir**.

Şu durumlarda uyarı verin:

- zamanlanmış yedekleme başarısız olduğunda;
- son başarılı yedek, tanımlanmış RPO'dan daha eski olduğunda;
- veritabanı dökümü başarısız olduğunda;
- uzak hedefe yükleme başarısız olduğunda;
- yedek deposu erişim bilgilerinin süresi dolduğunda;
- yedek boyutu şüpheli biçimde değiştiğinde;
- temizleme veya saklama görevi başarısız olduğunda.

«Cron çalıştı» ifadesini kullanılabilir bir yedeğin var olduğunun kanıtı saymayın.

RPO/RTO, saklama süresi, bağımsız kopyalar ve geri yükleme tatbikatları için [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}}) sayfasını kullanın.

## Günlükleri metriklerle ilişkilendirin {#correlate-logs-with-metrics}

Metrikler **neyin değiştiğini**, günlükler ise çoğu zaman **neden değiştiğini** gösterir.

Aynı zaman aralığını şu kaynaklarda birlikte inceleyin:

- Nginx/Apache erişim ve hata günlükleri;
- PHP-FPM ve çalışma ortamı günlükleri;
- uygulama günlükleri;
- veritabanı günlükleri;
- sistem günlüğü;
- kimlik doğrulama günlükleri;
- yedekleme ve görev günlükleri.

Örnek:

- 14:03'te CPU kullanımı yükselir;
- 14:03'te 5xx hataları artar;
- uygulama günlüğünde veritabanı zaman aşımları görülür;
- veritabanı günlüğünde kilit çekişmesi görülür.

Bu, genel bir «CPU yüksek» uyarısından daha fazla yol gösterir.

Olayları incelemeye yetecek günlük geçmişini tutun; ancak günlüklerin canlı sistemin dosya sistemini doldurmasına izin vermeyin.

## Müdahaleye yönelik uyarılar oluşturun {#build-actionable-alerts}

Uyarı, sorumlu kişiye neyin bozulduğunu ve önce neyi kontrol etmesi gerektiğini söylemelidir.

Şunları tercih edin:

- **uyarı** — kullanıcı etkilenmeden önce inceleyin;
- **kritik** — kullanıcı etkisi veya yakın arıza riski var;
- süre ve gecikmeli tetikleme — bir saniyelik yükselişte acil çağrı göndermeyin;
- gruplama ve yinelenenleri ayıklama — tek kesinti için 40 bildirim göndermeyin;
- etkilenen sunucu veya hizmetin açık adı;
- gösterge paneli, günlük veya işlem rehberi bağlantısı;
- bilinen ilk adım ve üst sorumluya aktarma yolu.

Prometheus Alertmanager, uyarıları gruplamak, yinelenenleri ayıklamak ve yönlendirmek için tasarlanmış bir sistem örneğidir.

### Evrensel eşiklerden kaçının {#avoid-universal-thresholds}

Eşikler iş yüküne uygun olmalıdır.

Makul başlangıç mantığı örnekleri:

- CPU: tek yükseliş yerine sürekli yüksek kullanım ile gecikme veya kuyruk belirtileri;
- RAM: yalnızca «kullanılan RAM > %80» yerine düşük kullanılabilir bellek ile swap veya OOM;
- disk: yeterli çalışma payı varken erken uyarı;
- TLS: süre dolmadan günler önce uyarı;
- HTTP: yanlış alarmlar önemliyse tekrarlanan hata veya birden fazla konumdan doğrulama;
- yedekleme: son başarının RPO'dan eski olması;
- 5xx ve gecikme: uygulamanın normal düzeyinden sürekli sapma.

Canlı sistemin normal davranışını gözlemledikten sonra ayarlayın.

## Bildirim yolunu bağımsız tutun {#keep-the-notification-path-independent}

Uyarıyı ileten sistem aynı olayda devre dışı kalıyorsa uyarı işe yaramaz.

Mümkünse önemli uyarıları VPS dışındaki bir yoldan gönderin:

- harici e-posta sağlayıcısı;
- harici sohbet veya bildirim hizmeti;
- barındırılan olay yönetimi aracı;
- başka bir arıza alanındaki izleme sunucusu.

Yalnızca aynı arızalı VPS üzerinde barındırılan SMTP sunucusuna veya gösterge paneline güvenmeyin.

## Her uyarının sorumlusu ve işlem rehberi olmalı {#every-alert-needs-an-owner-and-runbook}

Bir uyarı oluşturmadan önce şu soruları yanıtlayın:

- kim alacak?
- kim müdahale etmeye yetkili?
- ilk tanılama adımı nedir?
- hangi gösterge paneli veya günlük açılmalı?
- ne zaman üst sorumluya aktarılmalı?
- ne zaman güvenle susturulabilir?
- mesai saatleri dışında ne olacak?

Müdahalenin sorumlusu yoksa izleme sistemi kesintiyi yalnızca bir bildirime dönüştürmüş olur.

Genel operasyon sorumluluğu kararı için [Yönetilen ve yönetilmeyen VPS karşılaştırması]({{< relref "managed-vs-unmanaged-vps.md" >}}) sayfasına bakın.

## İzleme sistemini gereken karmaşıklığa göre seçin {#choose-the-monitoring-stack-by-complexity}

Popüler diye büyük bir gözlemlenebilirlik platformu kurmayın.

### Başlangıç katmanı olarak sağlayıcı paneli {#provider-dashboard-as-a-starting-layer}

VPS sağlayıcısı CPU, RAM, disk veya ağ geçmişi sunuyorsa bunu kullanışlı bir sunucu düzeyi başlangıç katmanı olarak değerlendirin.

Sağlayıcı tarafındaki altyapı grafiklerini eksiksiz web sitesi izlemesiyle karıştırmayın. Bunlar sağlayıcı dışından genel HTTP(S) yolunu, uygulama içeriğini, veritabanı sağlığını, arka plan görevlerini, TLS yenilemeyi veya uyarı sorumluluğunu doğrulamayabilir.

Sağlayıcı izlemesini kanıt kaynaklarından biri olarak kullanın; ardından iş yükünün gerektirdiği harici ve uygulama düzeyi kontrolleri ekleyin.

### Tek VPS için hafif yaklaşım {#lightweight-single-vps-path}

Küçük ve uygulanabilir bir kurulum şunları birleştirebilir:

- harici erişilebilirlik izleyicisi;
- Netdata veya başka bir sunucu metriği ajanı ve gösterge paneli;
- sistem ve uygulama günlükleri;
- bildirimler.

Bir yöneticinin bir veya birkaç VPS yönettiği durumda uygundur.

### Prometheus / Grafana yaklaşımı {#prometheus--grafana-path}

Şunlara ihtiyaç duyduğunuzda yararlıdır:

- birden fazla sunucunun metrikleri;
- daha uzun geçmiş saklama;
- özel sorgular;
- hizmet ve exporter metrikleri;
- ortak gösterge panelleri;
- yapılandırılmış uyarı kuralları.

Node Exporter Linux sunucu metriklerini sağlar; Prometheus bunları saklar ve sorgular; Grafana görselleştirir; Alertmanager uyarıları yönlendirebilir, gruplayabilir ve yinelenenleri ayıklayabilir.

### Barındırılan izleme hizmeti yaklaşımı {#hosted-monitoring-path}

Şu durumlarda yararlıdır:

- izleyicinin VPS'nizden ve sağlayıcınızdan bağımsız olması gerekiyorsa;
- yönetilecek izleme altyapısını azaltmak istiyorsanız;
- yönetilen bildirimler ve nöbetçi ekip entegrasyonları değerliyse.

İzleme sisteminin kendisi de canlı altyapıdır. Karmaşıklığını azalttığı riskle orantılı tutun.

## İzleme sisteminin güvenliğini sağlayın {#secure-the-monitoring-stack}

İzleme ajanları ve gösterge panelleri hassas operasyon verilerini açığa çıkarabilir.

Şunları koruyun:

- gösterge panelleri;
- exporter'lar;
- metrik uç noktaları;
- API erişim anahtarları;
- bildirim webhook'ları;
- günlük depolama sistemleri.

Açıkça tanımlanmış güvenli bir erişim modeli olmadan Prometheus, Node Exporter, Grafana veya yönetim panellerini internete açık bırakmayın.

Uygun olduğunda güvenlik duvarı, özel ağ veya ters proxy kimlik doğrulaması kullanın.

İzleme, güvenlik sıkılaştırmasının yerine geçmez. Sunucunun temel önlemleri için [VPS güvenlik kontrol listesi]({{< relref "vps-security-checklist.md" >}}) sayfasını kullanın.

## İzlemenin kaynak yükü önemlidir {#monitoring-overhead-matters}

İzleme şunları tüketir:

- RAM;
- CPU;
- metrik ve günlük saklamak için disk;
- ağ;
- yedekleme kapasitesi.

Küçük bir ajan genellikle az kaynak tüketir; ancak uzun süre saklanan metrikler ve günlükler ciddi bir depolama iş yüküne dönüşebilir.

İzleme sisteminin kendisini de izleyin:

- ajan ve hizmet sağlığı;
- metrik toplama hataları;
- depolama büyümesi;
- saklama süresi;
- bildirimlerin iletilmesi.

Gözlemlenebilirlik araçlarının korumaları gereken diski doldurmasına izin vermeyin.

## Kapasite planlamasında eğilimleri kullanın {#use-trends-for-capacity-planning}

Geçmiş izleme verileri, bir sonraki boyutlandırma kararı için en iyi kanıttır.

Şu soruları eğilimlerle yanıtlayın:

- CPU doygunluğu sürekli mi, ara sıra mı?
- kullanılabilir RAM haftalar içinde azalıyor mu?
- gerçek iş yükünde swap veya OOM görülüyor mu?
- disk kullanımı ne kadar hızlı büyüyor?
- yoğun trafikte veritabanı gecikmesi artıyor mu?
- PHP veya uygulama kuyrukları oluşuyor mu?
- yedekleme ve içe aktarma görevleri öngörülebilir kaynak çekişmesi yaratıyor mu?

Bir gösterge paneli kısa süreliğine kırmızıya döndü diye kaynakları artırmayın.

**Optimize edilmiş gerçek iş yükü** bir kaynağı tekrar tekrar tüketiyorsa veya mimari bağımsız ölçekleme gerektiriyorsa ölçekleyin.

İzleme kanıtını kaynak kararına dönüştürmek için [Web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) sayfasını kullanın.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS yapılandırmalarını inceleyin</a>
</p>
<p><small>Açıklama: Editörün VDSina ile profesyonel bir ilişkisi vardır. Bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Boyutlandırma kararını izleme verileri yönlendirmelidir; bu sayfa VDSina'nın yukarıdaki izleme araçlarını yönetilen hizmet olarak sunduğunu iddia etmez.</small></p>

## Birden fazla web sitesini iki düzeyde izleyin {#monitor-multiple-websites-at-two-levels}

Çok siteli bir VPS'de şunları izleyin:

### Sunucu düzeyi {#server-level}

- CPU, RAM ve swap;
- disk, inode ve G/Ç;
- veritabanı;
- ağ;
- temel hizmetler.

### Site düzeyi {#site-level}

- her önemli ana makine adı;
- TLS;
- yanıt süresi;
- 5xx hataları;
- uygulama ve görev hataları;
- mevcutsa siteye özel günlükler veya işçi süreçleri üzerindeki baskı.

Tek bir sanal sunucu kaydı, sertifika veya web sitesi bozukken sunucu sağlıklı olabilir.

Birlikte barındırma ve arıza alanı kararı için [Birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) sayfasını kullanın.

## VPS izleme kontrol listesi {#vps-monitoring-checklist}

| Sinyal | Başarı koşulu |
|---|---|
| Harici erişilebilirlik | önemli ana makine adı VPS dışından kontrol ediliyor |
| HTTP sağlığı | beklenen durum, içerik veya sağlık uç noktası doğrulanıyor |
| CPU | sürekli kullanım, yük ve süreç bazında geçmiş saklanıyor |
| RAM | kullanılabilir bellek, swap ve OOM görülebiliyor |
| Disk | kapasite ve büyüme izleniyor |
| Inode | inode tükenmesi ayrı izleniyor |
| G/Ç | depolama önemliyse gecikme ve G/Ç bekleme süresi görülebiliyor |
| Ağ | aktarım hızı, hatalar ve ağ yolu sorunlarının belirtileri gözlenebiliyor |
| Hizmetler | web, çalışma ortamı, veritabanı ve işçi süreçlerinin sağlığı izleniyor |
| Veritabanı | uygulamayı ilgilendiren erişilebilirlik, gecikme ve bağlantılar görülebiliyor |
| Görevler | cron, kuyruk ve arka plan hataları veya birikimler gözlenebiliyor |
| TLS/DNS | süre dolumu ve çözümleme hataları tespit edilebiliyor |
| Yedekler | son başarılı yedeğin yaşı ve görev hataları izleniyor |
| Günlükler | olayları ilişkilendirmek için web, uygulama, veritabanı ve sistem günlükleri mevcut |
| Uyarılar | uyarı/kritik düzeyleri ile süre ve gecikmeli tetikleme kuralları ayarlandı |
| Bildirim | önemli uyarılar VPS'nin arıza alanının dışına iletiliyor |
| Sorumluluk | belirli müdahale sorumlusu ve ilk adım rehberi var |
| Saklama | eğilim ve kök neden analizi için yeterli metrik ve günlük geçmişi var |
| Güvenlik | izleme uç noktaları ve paneller istemeden herkese açılmamış |
| Kapasite | eğilimler sonraki optimizasyon veya ölçekleme kararını besliyor |

## Teknik kaynaklar {#technical-references}

- Prometheus — Node Exporter ile Linux sunucu metriklerini izleme
- Prometheus — Alertmanager
- Uptime Kuma — Resmî proje
- [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}})
- [VPS güvenlik kontrol listesi]({{< relref "vps-security-checklist.md" >}})

## Sık sorulan sorular {#faq}

### VPS'de neleri izlemeliyim? {#what-should-i-monitor-on-a-vps}

En azından web sitesinin dışarıdan erişilebilirliğini, CPU'yu, kullanılabilir RAM/swap/OOM'u, disk kapasitesini, inode'ları, temel hizmetleri, uygulama sağlığını, TLS süresini, yedeklerin güncelliğini ve uyarı iletimini izleyin.

### CPU'nun %80'i aşması her zaman kötü mü? {#is-cpu-over-80-always-bad}

Hayır. Kısa süreli yüksek CPU kullanımı normal olabilir. Sürekli kullanımı; yük, istek gecikmesi, kuyruklar ve işi yapan süreçle birlikte inceleyin.

### Linux'ta RAM neden neredeyse dolu? {#why-is-linux-ram-almost-full}

Linux boş belleği önbellek için kullanır. Yalnızca kullanılan yüzdeye göre alarm vermek yerine kullanılabilir belleği, swap etkinliğini, OOM olaylarını ve süreçlerin büyümesini izleyin.

### Disk sorunları için neleri izlemeliyim? {#what-should-i-monitor-for-disk-problems}

Dosya sistemi kapasitesini, inode kullanımını, depolama büyümesini ve G/Ç gecikmesi veya bekleme süresini izleyin. Yalnızca boş GB miktarı bütün disk arızası türlerini kapsamaz.

### Erişilebilirlik izleme için ping yeterli mi? {#is-ping-enough-for-uptime-monitoring}

Hayır. Web sitesi, veritabanı veya TLS yolu bozukken ping başarılı olabilir. Kullanıcıya görünen hizmet sağlığı için HTTP(S), uygulama ve hizmet kontrolleri kullanın.

### Erişilebilirlik izleyicisi aynı VPS'de çalışmalı mı? {#should-the-uptime-monitor-run-on-the-same-vps}

Tek izleyici olarak çalışmamalı. VPS'nin veya ağın tamamen arızalanması, izleyiciyi de web sitesiyle birlikte devre dışı bırakabilir. En azından kritik erişilebilirlik ve bildirim yolunu bu arıza alanının dışında tutun.

### En iyi VPS izleme aracı hangisi? {#which-vps-monitoring-tool-is-best}

Herkes için en iyi tek araç yoktur. Tek VPS için harici erişilebilirlik kontrolü ve hafif bir sunucu metriği ajanı yeterli olabilir. Sunucu filosu için Prometheus, Grafana ve Alertmanager anlamlı olabilir. Gereken görünürlük, saklama süresi ve yönetim karmaşıklığına göre seçin.

### Tek VPS için Prometheus ve Grafana gerekir mi? {#do-i-need-prometheus-and-grafana-for-one-vps}

Şart değildir. Uzun dönemli metrikler, özel sorgular ve birden fazla sunucu gerektiğinde güçlü araçlardır; ancak küçük bir kurulumda hafif ajan ve harici erişilebilirlik izleme yeterli olabilir.

### Yedekleri nasıl izlemeliyim? {#how-should-i-monitor-backups}

Başarısız görevlerde ve son başarılı yedeğin yaşı RPO'yu aştığında uyarı verin. Ardından kurtarılabilirliği ayrıca geri yükleme testleriyle doğrulayın.

### İzleme ne zaman VPS kaynaklarını artırmayı gerektirmeli? {#when-should-monitoring-trigger-a-vps-upgrade}

Geçmiş veriler, optimize edilmiş gerçek iş yükünün CPU, RAM, depolama/G/Ç veya başka bir kaynağı tekrar tekrar tükettiğini gösterdiğinde. Tek bir anlık yükseliş yeterli kanıt değildir.
