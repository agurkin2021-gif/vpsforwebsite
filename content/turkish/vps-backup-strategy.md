---
title: "VPS yedekleme stratejisi"
description: "VPS yedekleme stratejisi: RPO ve RTO hedeflerini belirleyin, sağlayıcı imajlarını bağımsız uzak yedeklerle tamamlayın, veritabanlarını ve gizli bilgileri koruyun, saklama sürelerini tanımlayın ve geri yükleme testleriyle kurtarmayı doğrulayın."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-yedekleme-stratejisi"
---

VPS yedekleme stratejisi, «günde bir kez anlık görüntü almayı açmak» değildir. Kullanılabilir bir kurtarma planı; **ne kadar veri kaybedilebileceğini (RPO), kurtarmanın ne kadar sürebileceğini (RTO), hangi verilerin korunması gerektiğini, bağımsız kopyaların nerede tutulduğunu, sürümlerin ne kadar saklandığını ve birinin bunları gerçekten geri yükleyip yüklemediğini** tanımlar.

Sağlam bir VPS planı genellikle sağlayıcı tarafında hızlı kurtarmayı, sunucu dışında bağımsız bir kopyayı ve uygulamayı dikkate alan veritabanı yedeklerini birleştirir. Kesin bileşim, verinin ne kadar hızlı değiştiğine ve kesintinin maliyetine bağlıdır.

Yedekleme stratejisinin de belirli bir sorumlusu olmalıdır. Görev hataları, geri yükleme testleri ve kurtarma kararlarından kimse sorumlu değilse önce yönetim modelini çözün: [Yönetilen ve yönetilmeyen VPS karşılaştırması]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Genel sunucu seçimi için [Web sitesi için VPS]({{< relref "_index.md" >}}) sayfasına bakın.

[Kısa yanıt](#quick-answer) · [Kontrol aracı](#vps-backup-strategy-checker) · [RPO / RTO](#start-with-rpo-and-rto) · [Yedekleme katmanları](#snapshot-image-file-backup-and-replication-are-different) · [3-2-1](#a-practical-3-2-1-model-for-vps) · [Geri yükleme testleri](#test-restores-and-measure-real-rto) · [VDSina](#how-vdsina-backups-fit-the-strategy) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

Uygulanabilir bir VPS kurtarma tasarımında birkaç katman bulunur:

| Katman | Temel görevi | Tek başına neyi kanıtlamaz? |
|---|---|---|
| **Sağlayıcı yedek imajı / anlık görüntü** | bütün sunucuyu hızla geri almak veya yeniden kurmak | sağlayıcı hesabı veya depolaması erişilemezken bağımsız kurtarma |
| **Veritabanı tutarlılığını koruyan yedek** | uygulama durumunu ve son yazılan verileri kurtarmak | tek başına eksiksiz sunucu yapılandırması |
| **Dosya ve yapılandırma yedeği** | yüklenen dosyaları, yapılandırmayı, uygulama verilerini ve seçili dosyaları geri yüklemek | bütün sunucuyu hızla kurtarma |
| **Bağımsız uzak kopya** | ana sağlayıcı, hesap veya sunucu arızasından kurtulmak | geri yükleme prova edilmedikçe kısa RTO |
| **Geri yükleme tatbikatı** | kopyaların, anahtarların ve işlem rehberinin çalıştığını kanıtlamak | izleme olmadan gelecekteki yedeklerin çalışmaya devam edeceği |

Sıradan web sitesi VPS kurulumlarının çoğunda iyi bir başlangıç şunları içerir:

- hızlı geri dönüş için sağlayıcı tarafında imaj veya anlık görüntü;
- dosya, yapılandırma ve veritabanının başka bir arıza alanında şifrelenmiş bağımsız yedeği;
- birden fazla geri yükleme noktası;
- kabul edilebilir veri kaybına göre seçilmiş veritabanı yedekleme sıklığı;
- düzenli geri yükleme testleri.

Bu, tek bir «yedekleme başarılı» durumuna güvenmekten daha yararlıdır.

## VPS yedekleme stratejisi kontrol aracı {#vps-backup-strategy-checker}

Bu araç, ihtiyaç duyduğunuz kurtarma mimarisini belirlemenize yardımcı olur. Kurtarma garantisi vermez.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-backup-strategy-checker-form">
  <div class="mb-6">
    <label for="bk-workload" class="form-label">İş yükü türü</label>
    <select id="bk-workload" class="form-input">
      <option value="static">Statik / tanıtım / nadiren değişen site</option>
      <option value="cms">WordPress / CMS / kurumsal web sitesi</option>
      <option value="transactional">WooCommerce / sipariş / üyelik / sık veri yazma</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rpo" class="form-label">Kabul edilebilir en fazla veri kaybı (RPO)</label>
    <select id="bk-rpo" class="form-input">
      <option value="24">24 saate kadar</option>
      <option value="4">4 saate kadar</option>
      <option value="1">1 saate kadar</option>
      <option value="lt1">1 saatten az</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rto" class="form-label">Kabul edilebilir en uzun kesinti (RTO)</label>
    <select id="bk-rto" class="form-input">
      <option value="24">24 saate kadar</option>
      <option value="4">4 saate kadar</option>
      <option value="1">Yaklaşık 1 saat</option>
      <option value="lt1">1 saatten az</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-offsite" class="form-label">Sunucu dışında / uzak konumda bağımsız kopya var mı?</label>
    <select id="bk-offsite" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-db" class="form-label">Veritabanı tutarlılığını koruyan yedekleme yöntemi doğrulandı mı?</label>
    <select id="bk-db" class="form-input">
      <option value="na">Uygulanamaz / veritabanı yok</option>
      <option value="no">Hayır / bilinmiyor</option>
      <option value="yes">Evet</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-restore" class="form-label">Yakın zamanda geri yükleme testi başarıyla tamamlandı mı?</label>
    <select id="bk-restore" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-creds" class="form-label">Yedek erişim bilgileri ve şifreleme kurtarma anahtarı VPS'den ayrı tutuluyor mu?</label>
    <select id="bk-creds" class="form-input"><option value="no">Hayır / bilinmiyor</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-versions" class="form-label">Birden fazla geri yükleme noktası ve saklanan sürüm geçmişi var mı?</label>
    <select id="bk-versions" class="form-input"><option value="no">Yalnızca son sürüm / bilinmiyor</option><option value="yes">Evet</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Yedekleme stratejisini kontrol edin</button>
</form>
<p id="vps-backup-strategy-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Sizin için gerçekten geçerli olan kurtarma gereksinimlerini seçin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-backup-strategy-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var workload = val("bk-workload");
    var rpo = val("bk-rpo");
    var rto = val("bk-rto");
    var offsite = val("bk-offsite") === "yes";
    var db = val("bk-db");
    var restore = val("bk-restore") === "yes";
    var creds = val("bk-creds") === "yes";
    var versions = val("bk-versions") === "yes";

    var criticalGap = !offsite || !restore || !creds || !versions || (db === "no");
    var result;

    if (criticalGap) {
      result = "KRİTİK YEDEKLEME EKSİKLERİ: strateji hâlâ doğrulanmamış veya bağımsız olmayan bir kurtarma yoluna bağlı. Uzak/bağımsız kopyalar, birden fazla geri yükleme noktası, ayrı tutulan kurtarma erişim bilgileri ve anahtarları, gerektiğinde veritabanı tutarlılığını koruyan yedekler ve gerçek bir geri yükleme testi ekleyin.";
    } else if (rto === "lt1" || rto === "1") {
      result = "KISA RTO / FELAKET KURTARMA MİMARİSİNİ YENİDEN KONTROL EDİN: yedekler doğru olsa bile elle yeniden kurulum bir saatlik kurtarma hedefini aşabilir. Tam kurtarma tatbikatının süresini ölçün; ölçülen RTO yetersizse otomasyon, hazır imajlar, kısmen hazır bekleyen yedek sistem veya iş yükünü ayırmayı değerlendirin.";
    } else if (workload === "transactional" || rpo === "lt1" || rpo === "1") {
      result = "İŞLEM YOĞUNLUĞU / SIK VERİTABANI YEDEKLEME YOLU: bağımsız kurtarma katmanlarını koruyun, ancak veritabanı koruma sıklığını gereken RPO'ya göre ayarlayın. Gecelik yedekleme, bir saatlik veri kaybı hedefini karşılayamaz.";
    } else {
      result = "TEMEL KURTARMA STRATEJİSİ: ana katmanlar mevcut. Sağlayıcının kurtarma noktalarıyla birlikte bağımsız uzak yedekleri koruyun, görev hatalarını izleyin, birden fazla sürüm saklayın ve süre ölçülen geri yükleme tatbikatlarını tekrarlayın.";
    }

    document.getElementById("vps-backup-strategy-result").textContent = result;
  });
});
</script>

## RPO ve RTO ile başlayın {#start-with-rpo-and-rto}

Stratejiyi iki sayı yönlendirmelidir.

### Kurtarma noktası hedefi — RPO {#recovery-point-objective--rpo}

RPO şu soruyu yanıtlar:

**İşletme en son oluşan verilerin ne kadarını kaybetmeyi göze alabilir?**

RPO hedefi:

- **24 saat** ise her gün başarıyla oluşturulan bir kurtarma noktası kabul edilebilir;
- **4 saat** ise günlük yedekler yetersizdir;
- **1 saat** ise değişen uygulama ve veritabanı durumu en az bu sıklıkta korunmalıdır;
- **dakikalar** düzeyindeyse sıradan zamanlanmış yedekler tek başına yeterli olmayabilir.

RPO, kesintiyle değil **veri kaybıyla** ilgilidir.

### Kurtarma süresi hedefi — RTO {#recovery-time-objective--rto}

RTO şu soruyu yanıtlar:

**Web sitesi veya hizmet en fazla ne kadar süre kullanılamaz kalabilir?**

Bir yedek RPO'yu karşılayıp RTO'yu karşılamayabilir.

Örnek:

- veritabanı her saat kopyalanır;
- son verilerdeki kayıp bir saatten azdır;
- ancak VPS'yi yeniden oluşturmak, verileri indirmek, veritabanını geri yüklemek ve siteyi doğrulamak altı saat sürer.

Bu strateji bir saatlik RPO'yu karşılayabilir; fakat gerçek RTO yaklaşık altı saattir.

NIST'in acil durum planlama rehberi, RPO'yu zamanda geri dönülecek kurtarma noktası, RTO'yu ise kabul edilebilir en uzun kullanılamama süresi olarak tanımlar. Araç seçmeden önce bu hedefleri belirleyin.

## Neler yedeklenmeli? {#what-should-be-backed-up}

Sunucuyu **yeniden oluşturulabilir** ve **durum bilgisi tutan/yerine konamaz** bileşenlere ayırın.

### Yeniden oluşturulabilir bileşenler {#rebuildable}

Genellikle koddan veya otomasyonla yeniden üretilebilir:

- temel işletim sistemi;
- paketler;
- Git'te zaten güvenle saklanan uygulama kodu;
- yeniden oluşturulabilen veya çekilebilen konteyner imajları;
- standart web sunucusu paketleri.

### Durum bilgisi tutan / yeniden oluşturulması zor bileşenler {#stateful--difficult-to-recreate}

Genellikle daha yüksek önceliklidir:

- veritabanları;
- kullanıcı yüklemeleri ve medya;
- yerel olarak barındırılıyorsa posta kutuları;
- yapılandırma;
- kurtarma için gereken ortam ayarları ve gizli bilgiler;
- yenilenmesi kolay değilse TLS ve özel anahtarlar;
- uygulamanın ürettiği veriler;
- kontrol paneli ve site yapılandırması;
- cron ve işçi süreçlerinin yapılandırması;
- DNS VPS'de barındırılıyorsa DNS bölge verileri;
- başka yerde saklanmayan özel betikler.

Siteyi başlatmak için gereken veritabanını veya gizli bilgileri unutup önbellekleri, geçici dosyaları ve yeniden üretilebilir çıktıları gelişigüzel kopyalayarak yedek kapasitesini harcamayın.

## Anlık görüntü, imaj, dosya yedeği ve çoğaltma farklıdır {#snapshot-image-file-backup-and-replication-are-different}

Bunları birbirinin yerine geçebilen yöntemler olarak görmeyin.

### Sağlayıcı anlık görüntüsü / sunucu imajı {#provider-snapshot--server-image}

Şunlar için yararlıdır:

- riskli bir güncellemeden sonra hızlı geri dönüş;
- bütün sunucuyu kurtarma;
- sanal makineyi klonlama veya yeniden oluşturma.

Zayıf yönleri:

- aynı sağlayıcı veya hesap arıza alanında bulunabilir;
- tek tek dosya veya site geri yüklemeyi desteklemeyebilir;
- uygulama ve veritabanı tutarlılığının yine anlaşılması gerekir;
- yalnızca son imajın tutulması çok az geçmiş sağlar.

### Dosya düzeyinde yedekleme {#file-level-backup}

Şunlar için yararlıdır:

- yüklenen dosyalar;
- yapılandırma;
- seçili uygulama verileri;
- seçerek geri yükleme.

restic veya Borg gibi araçlar, uzak depolarda şifrelenmiş ve sürümlendirilmiş yedekler saklayabilir.

### Veritabanı yedekleme {#database-backup}

Veritabanı motorunu dikkate alan bir yöntem kullanın:

- mantıksal döküm;
- veritabanının kendi yedekleme aracı;
- uygulama tutarlılığını koruyan anlık görüntü veya süreç.

Çalışan veritabanı dosyalarını kopyalamanın kullanılabilir bir veritabanı yedeği ürettiğini varsaymayın.

### Çoğaltma / yedekte bekleyen sistem {#replication--standby}

Çoğaltma, kurtarma süresini veya veri kaybını azaltabilir; ancak tek başına geçmişe dönük yedek değildir.

Yanlış silme, bozulma veya uygulama hatası da çoğaltılabilir.

Gerektiğinde erişilebilirlik ve RTO için çoğaltma veya yedekte bekleyen sistem kullanın; geçmiş bir duruma dönmek için de sürümlendirilmiş yedekler tutun.

## VPS için uygulanabilir 3-2-1 modeli {#a-practical-3-2-1-model-for-vps}

Yaygın 3-2-1 modeli şunu ifade eder:

- önemli verilerin **3 kopyası**;
- **2 farklı depolama veya arıza biçimi**;
- **uzak konumda / ana arıza alanının dışında 1 kopya**.

VPS için pratik bir uygulama şöyle olabilir:

1. VPS üzerindeki canlı veriler;
2. hızlı kurtarma için sağlayıcı yedek imajı;
3. bağımsız bir hedefte şifrelenmiş uzak dosya ve veritabanı yedeği.

Amaç bir sloganı kelimesi kelimesine karşılamak değildir. Tek bir olayın hem canlı verileri hem de bütün kurtarma kopyalarını yok etmesini önlemektir.

Arıza alanı örnekleri:

- VPS dosya sistemi;
- sağlayıcının yedek depolaması;
- sağlayıcı hesabı;
- ayrı bir nesne depolama hesabı veya sağlayıcısı;
- çevrimdışı veya değiştirilemez kopya.

VPS'yi kontrol eden bir saldırgan aynı erişim bilgileriyle bütün yedekleri silebiliyorsa kopyalar anlamlı biçimde bağımsız değildir.

## Veritabanı tutarlılığını koruyan yedekler {#database-consistent-backups}

Site çalışırken veritabanının durumu değişir.

Geçerli bir stratejide veritabanı motorunun nasıl korunduğu bilinmelidir.

WordPress/MySQL/MariaDB için bu yöntemler şunlar olabilir:

- mantıksal dökümler;
- veritabanının kendi yedekleme araçları;
- koordineli anlık görüntüler;
- veritabanı tutarlılığını açıkça ele alan yedekleme yazılımı.

PostgreSQL için RPO gerektirdiğinde PostgreSQL'e uygun yedekleme ve belirli bir zamana kurtarma (PITR) yöntemlerini kullanın.

Belirleyici olan aracın adı değildir. Geri yüklenen veritabanının kendi içinde tutarlı ve kullanılabilir olmasıdır.

WordPress'e özel uygulama durumu ve işlemler için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) sayfasına bakın.

Şunları test edin:

- döküm veya yedekleme tamamlanıyor;
- dosya boş değil;
- geri yükleme veya içe aktarma başarılı;
- örnek tablolar ve kayıtlar mevcut;
- uygulama bağlanabiliyor ve kritik okuma/yazma işlemlerini yapabiliyor.

## İşlem yapan siteler farklı bir RPO gerektirir {#transactional-sites-need-a-different-rpo}

Bir tanıtım sitesi bir günlük kopyayla çalışabilir.

Sipariş alan bir mağaza bunu kabul edemeyebilir.

WooCommerce, üyelik, faturalandırma veya sipariş sistemlerinde en son oluşan hangi verilerin ne kadarının kaybedilebileceğini belirleyin:

- siparişler;
- ödemeler;
- stok;
- müşteriler;
- üyelikler;
- form gönderimleri;
- yüklenen dosyalar.

Mağaza her saat sipariş alıyorsa gecelik veritabanı yedeği çok sayıda işlemin kaybolmasına yol açabilir.

Mağaza iş yükü için [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) sayfasını kullanın. Buradaki yedekleme takvimi, kabul edilebilir işlem kaybı süresine göre seçilmelidir.

## Yedekleme sıklığı ve saklama süresi {#backup-frequency-and-retention}

Yedekler arasındaki süre, korunan veri sınıfının RPO hedefini aşmamalıdır.

Farklı veriler için farklı takvimler kullanılabilir:

- veritabanı: sık;
- yüklenen dosyalar: sık veya olaya bağlı;
- işletim sistemi ve yapılandırma: önemli değişikliklerden sonra ve zamanlanmış olarak;
- tam sağlayıcı imajı: daha seyrek, ancak riskli değişikliklerin öncesinde yararlı.

Saklama süresi, geç fark edilen sorunlara karşı koruma sağlar.

Örnek bir düzen şunları tutabilir:

- yakın geçmişteki saatlik geri yükleme noktaları;
- birkaç günlük kopya;
- birkaç haftalık kopya;
- seçili aylık kopyalar.

Kesin saklama süresi şunlara göre belirlenmelidir:

- işletmenin kurtarma ihtiyaçları;
- depolama maliyeti;
- verinin değişme hızı;
- uyum ve yasal gereksinimler;
- bozulma veya ihlalin ne kadar süre fark edilmeden kalabileceği.

Yalnızca «son sürümü» tutmayın.

## Sunucu dışında bağımsız bir hedef kullanın {#keep-an-independent-off-server-destination}

Aynı VPS diskindeki yedek şunlara karşı korumaz:

- disk veya dosya sistemi kaybı;
- sunucunun silinmesi;
- root hesabının ele geçirilmesi;
- fidye yazılımı;
- hesap üzerinde yapılan hata;
- sağlayıcı tarafında sanal makinenin kaybı.

Kurtarma verilerini VPS dışına taşıyın veya doğrudan aktarın.

Olası hedefler:

- nesne depolama;
- başka bir yedekleme hizmeti veya sağlayıcısı;
- yalnızca yedekler için kullanılan başka bir VPS;
- çevrimdışı veya erişimi kontrollü depolama.

Uygulanabildiğinde sağlayıcı ve hesap erişim bilgilerini ayırın.

## Yedekleri şifreleyin ve kurtarma anahtarını koruyun {#encrypt-backups--and-protect-the-recovery-key}

Hassas yedek verilerini uygun olduğunda aktarım sırasında ve depolandıkları yerde şifreleyin.

Ancak şifreleme, kurtarma için yeni bir bağımlılık oluşturur.

Yedek parolası veya anahtarının **tek kopyasını** şuralarda tutmayın:

- yalnızca VPS üzerinde;
- erişilemez hale gelebilecek aynı parola kasasında veya hesapta;
- yalnızca şifrelenmiş yedeğin içinde.

Kurtarma erişim bilgilerini ve anahtarlarını güvenli, bağımsız bir yerde tutun. Geri yükleme tatbikatlarında anahtarlara erişilebildiğini de kontrol edin.

## Yedek erişim bilgilerini ve silme yetkilerini ayırın {#separate-backup-credentials-and-deletion-rights}

Canlı sunucunun ele geçirilmesi, saldırgana bütün kurtarma kopyalarını silme iznini otomatik olarak vermemelidir.

Şunları tercih edin:

- kapsamı sınırlandırılmış yedekleme erişim bilgileri;
- depolama destekliyorsa geniş silme yetkileri olmadan yazma erişimi;
- ayrı yönetici erişim bilgileri;
- uygun olduğunda saklama kilidi veya değiştirilemezlik;
- yüksek değerli veriler için çevrimdışı veya ağdan fiziksel olarak ayrılmış kopya.

Kesin tasarım depolama hizmetine bağlıdır.

Yedeklerin aynı zamanda bir güvenlik kontrolü olmasının nedenlerinden biri budur; [VPS güvenlik kontrol listesi]({{< relref "vps-security-checklist.md" >}}) sayfasına bakın.

## Yedekleme görevlerini izleyin {#monitor-backup-jobs}

Otomasyon, yedeklemelerin unutulmasını azaltır; ancak bozuk otomasyon sessizce başarısız olabilir.

Şunları izleyin:

- son başarılı yedekleme zamanı;
- başarısız veya kısmen tamamlanmış görevler;
- yedek deposunun veya depolamanın erişilebilirliği;
- erişim bilgilerinin süresinin dolması;
- yerel hazırlık öncesinde boş disk alanı;
- uzak yedek depolama kotası;
- veritabanı döküm hataları;
- yedekleme süresindeki değişiklikler;
- olağandışı küçük yedek boyutu;
- saklama ve eski yedekleri temizleme hataları.

Yeşil cron veya hizmet durumu, komutun çalıştığını gösterir. Geri yüklemenin çalıştığını kanıtlamaz.

Genel sunucu ve hizmet uyarı tasarımı [VPS izleme]({{< relref "vps-monitoring.md" >}}) sayfasında ele alınır; yedekleme görevlerinin sağlığı ise kurtarma stratejisinin bir parçasıdır.

## Geri yüklemeyi test edin ve gerçek RTO'yu ölçün {#test-restores-and-measure-real-rto}

Bir yedek, geri yüklenebildiğinde güvenilirlik kazanır.

Kurtarma tatbikatlarını yalıtılmış, temiz bir hedefte yapın.

Sürecin yeterli bölümünü test edin:

1. yeni bir VPS veya test ortamı oluşturun;
2. doğru yedekleme noktasını alın;
3. şifreleme ve yedek deposu erişim bilgilerini alın;
4. dosyaları ve yapılandırmayı geri yükleyin;
5. veritabanını geri yükleyin veya içe aktarın;
6. gerekli gizli bilgileri ve sertifikaları geri yükleyin;
7. hizmetleri ve ağı yapılandırın;
8. uygulamayı başlatın;
9. önemli sayfaları ve işlemleri test edin;
10. arka plan görevlerini ve entegrasyonları doğrulayın;
11. geçen kurtarma süresini ölçün.

Ölçülen sonucu kaydedin.

İşletmenin RTO hedefi dört saatken test sekiz saat sürüyorsa bütün dosyalar başarıyla geri yüklense bile yedekleme stratejisi iş gereksinimini karşılamamıştır.

NIST rehberi düzenli yedek oluşturmayı, geri yükleme testlerini ve kurtarma tatbikatlarını vurgular.

## Geri yüklemenin kapsamı önemlidir {#restore-granularity-matters}

İyi bir strateji, karşılaştığınız arıza türünü çözebilmelidir.

### Tek dosya veya site kurtarma {#single-filesite-recovery}

Şu durumlarda gerekir:

- yüklenen bir dosyanın silinmesi;
- yapılandırmanın bozulması;
- bir sitenin ele geçirilmesi;
- tek bir veritabanı veya sorunlu tablonun kurtarılması.

### Bütün sunucuyu kurtarma {#full-server-recovery}

Şu durumlarda gerekir:

- çalışmayan veya silinmiş VPS;
- dosya sistemi arızası;
- ciddi güvenlik ihlali;
- sağlayıcı veya sunucu değişimi.

Tek yedek tam disk imajıysa bir dosyayı geri yüklemek zor olabilir.

Tek yedek seçili dosyalardan oluşuyorsa bütün VPS'yi yeniden kurmak çok uzun sürebilir.

Yöntemleri katmanlar halinde birleştirin.

## Birden fazla web sitesinde site düzeyinde geri yükleme gerekir {#multiple-websites-need-site-level-restore}

Çok siteli VPS'de kurtarmayı, A sitesini düzeltmenin B/C/D sitelerini de otomatik olarak dünkü duruma döndürmesine yol açacak şekilde tasarlamayın.

Şunları ayrı ayrı geri yükleyebilen yedekleri tercih edin:

- tek belge kök dizini;
- tek veritabanı;
- tek panel veya kullanıcı;
- tek bir yüklenen dosya grubu;
- yalnızca gerektiğinde bütün VPS.

Mimari ve arıza alanı kararı için [Birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) sayfasına bakın.

## Yedeklemeler de kesintiye neden olabilir {#backups-can-cause-outages-too}

Yedekleme işlemleri kaynak tüketir.

Olası etkiler:

- veritabanı dökümünün CPU kullanımı;
- sıkıştırmanın CPU kullanımı;
- okuma G/Ç işlemleri;
- geçici disk kullanımı;
- nesne depolamaya yükleme bant genişliği;
- önbellek verilerinin yerinden edilmesi;
- yedeklemenin içe aktarma, tarama veya trafik zirveleriyle çakışması.

VPS'de yalnızca 10 GB boş alan varken 30 GB yerel arşiv oluşturmaktan kaçının.

Uygulanabildiğinde:

- yedekleri doğrudan sunucu dışına aktarın;
- geçici disk kullanımını izleyin;
- ağır yedekleme işlerini yoğun trafik saatlerinin dışına planlayın;
- araç destekliyorsa hız sınırlaması uygulayın;
- yedekleme süresini ölçün.

## VDSina yedekleri stratejiye nasıl dahil edilir? {#how-vdsina-backups-fit-the-strategy}

VDSina'nın herkese açık belgeleri şu anda birkaç yararlı kurtarma işlevi açıklıyor:

- elle oluşturulan sunucu yedek kopyaları;
- zamanlanmış yedekler;
- yedeği alındığı sunucuya geri yükleme;
- yedekten yeni sunucu oluşturma;
- sunucuyu klonlama;
- yedek imajını indirme.

İndirme belgesinde yedek dosyası adı şu biçimde gösterilir:

`vXXX.backup.hosted-by-vdsina.com.img.gz`

İndirilebilir imaj yararlı bir taşınabilirlik katmanıdır; kurtarma kopyasının yalnızca sağlayıcı panelinde kalması gerekmez.

Ancak:

- sağlayıcı imajını bütün strateji olarak değil, **tek bir katman** olarak değerlendirin;
- seçtiğiniz kurtarma ortamının indirilen imajı nasıl kullandığını test edin;
- her hipervizörün imajı dönüştürmeden doğrudan kullanabileceğini varsaymayın;
- seçerek kurtarma için uygulama, dosya ve veritabanı yedekleri tutun;
- risk gerektiriyorsa bağımsız bir arıza alanında kopya saklayın.

VDSina'nın kendi hizmet koşulları, yedeklerden müşterinin sorumlu olduğunu açıkça belirtir; düzenli yedekleme ve dönemsel geri yükleme testleri önerir.

Sağlayıcı yedeğinden yeni VDSina sunucusu oluştururken soru-cevap belgeleri, yedek ve yeni sunucunun veri merkezi konumu ve yeterli disk kotası gibi sağlayıcı kısıtlamalarına uyması gerektiğini belirtir. Geri yüklemeden sonra ağ ayarlarının da düzenlenmesi gerekebilir.

Yedeklemeyi taşımayla karıştırmayın. Yedek, taşımada bir güvence olabilir; ancak canlı geçiş, son yazılan veriler, DNS ve geri dönüş ayrı konulardır: [Web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS yedekleme seçeneklerini inceleyin</a>
</p>
<p><small>Açıklama: Editörün VDSina ile profesyonel bir ilişkisi vardır. Bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Sağlayıcının yedekleme özellikleri, bağımsız kurtarma stratejisinin veya geri yükleme testlerinin yerine geçmez.</small></p>

## Kurtarma işlem rehberi {#recovery-runbook}

Kesinti yaşanmadan önce kurtarma sürecini yazın.

En azından şunları kaydedin:

- yedek hedefleri;
- geri yükleme noktalarının adlandırılması ve saklanması;
- yedek deposu erişim bilgileri;
- şifreleme anahtarının kurtarılacağı konum;
- hangi verilerin veritabanı, dosya veya yapılandırma olduğu;
- yeni sunucu oluşturma adımları;
- yazılım ve çalışma ortamı sürümleri;
- geri yükleme sırası;
- DNS ve ağ adımları;
- harici entegrasyonlar ve webhook'lar;
- kabul testleri;
- kurtarma veya geri dönüş kararını kimin verdiği.

İşlem rehberini VPS erişilemezken de ulaşılabilecek bir yerde tutun.

## VPS yedekleme kontrol listesi {#vps-backup-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| RPO | kabul edilebilir en uzun veri kaybı aralığı tanımlı |
| RTO | kabul edilebilir en uzun kesinti tanımlı |
| Veri envanteri | veritabanı, yüklemeler, yapılandırma, gizli bilgiler ve diğer durum verileri sınıflandırıldı |
| Sağlayıcı kurtarması | imaj ve anlık görüntü takvimi biliniyor |
| Veritabanı | veritabanı motoruna uygun, geri yüklenebilir yedekleme yöntemi var |
| Uzak kopya | VPS'nin arıza alanı dışında bağımsız kurtarma kopyası var |
| Erişim bilgileri | yedek hesabının kapsamı sınırlı ve canlı sistemden ayrı |
| Şifreleme | hassas yedekler uygun olduğunda şifreleniyor |
| Anahtar kurtarma | kurtarma anahtarı veya parolası arızalanan VPS'nin dışında saklanıyor |
| Saklama | geçmişe ait birden fazla geri yükleme noktası var |
| İzleme | başarısız, kısmi veya güncelliğini yitirmiş yedekleme görevleri tespit ediliyor |
| Disk ve G/Ç | yedekleme süreci canlı sistemin diskini sessizce dolduramıyor veya sisteme aşırı yük bindiremiyor |
| Seçerek kurtarma | gerektiğinde dosya, site veya veritabanı geri yüklenebiliyor |
| Tam kurtarma | VPS veya hizmetin tamamını yeniden kurma yolu var |
| Geri yükleme testi | yalıtılmış ortamda geri yükleme başarıyla tamamlandı |
| Ölçülen RTO | gerçek kurtarma süresi kaydedildi ve hedef içinde |
| İşlem rehberi | kurtarma sırası, erişim bilgileri, DNS ve kabul testleri belgelendi |
| Sorumlu | yedekleme ve geri yüklemeden sorumlu kişi veya ekip belirli |

## Teknik kaynaklar {#technical-references}

- NIST SP 800-34 Rev.1 — RPO/RTO ve acil durum planlaması
- NIST SP 1339 — Yedek oluşturma, test etme ve kurtarma tatbikatları
- Ubuntu — restic yedekleme ve geri yükleme aracı
- Ubuntu — BorgBackup
- VDSina hizmet koşulları — Müşterinin yedekleme sorumluluğu
- VDSina — Sunucu yedeği, geri yükleme ve yedekten yeni sunucu
- VDSina — Zamanlanmış yedekler
- VDSina — Sunucu yedeğini indirme ve kullanma

## Sık sorulan sorular {#faq}

### İyi bir VPS yedekleme stratejisi nasıl olmalı? {#what-is-a-good-vps-backup-strategy}

RPO/RTO hedeflerini tanımlayın, bağımsız kurtarma kopyaları tutun, veritabanlarını uygulama tutarlılığını koruyan bir yöntemle yedekleyin, birden fazla sürüm saklayın, başarısız görevleri izleyin ve düzenli olarak temiz bir test ortamına geri yükleyin.

### VPS anlık görüntüsü yeterli mi? {#is-a-vps-snapshot-enough}

Tek kurtarma katmanı olarak yeterli değildir. Sağlayıcı anlık görüntüsü veya imajı hızlı geri dönüş ve bütün sunucuyu kurtarmak için yararlıdır; ancak aynı sağlayıcı veya hesap arıza alanını paylaşabilir ve seçerek geri yükleme için daha az kullanışlıdır.

### VPS için 3-2-1 ne anlama gelir? {#what-does-3-2-1-mean-for-a-vps}

Canlı verilerle birlikte bağımsız depolama ve arıza alanlarında birden fazla kurtarma kopyası tutun. En az bir kopya, ana VPS veya sağlayıcının arıza yolunun dışında olsun.

### VPS'yi ne sıklıkta yedeklemeliyim? {#how-often-should-i-back-up-a-vps}

Sıklığı her veri türünün RPO hedefine göre seçin. Statik site günlük kopyaları kabul edebilir; işlem yoğun veritabanı ise saatlik veya daha sık koruma gerektirebilir.

### RPO ile RTO arasındaki fark nedir? {#what-is-the-difference-between-rpo-and-rto}

RPO, en son verilerde kabul edilebilir en fazla kayıptır. RTO ise hizmet geri gelene kadar kabul edilebilir en uzun kesintidir.

### Bütün VPS'yi mi, yalnızca web sitesi dosyalarını mı yedeklemeliyim? {#should-i-back-up-the-whole-vps-or-only-website-files}

Genellikle iki katman da yararlıdır. Sunucu imajı tam kurtarmayı hızlandırır; dosya ve veritabanı yedekleri ise seçerek ve uygulama tutarlılığını koruyarak geri yüklemeyi kolaylaştırır.

### MySQL veya PostgreSQL'i nasıl güvenle yedeklerim? {#how-do-i-back-up-mysql-or-postgresql-safely}

Veritabanı motoruna uygun mantıksal döküm, yerel yedekleme aracı veya koordineli, uygulama tutarlılığını koruyan bir yöntem kullanın. Ardından yalıtılmış test ortamına geri yükleyerek veya içe aktararak çalıştığını kanıtlayın.

### Yedekler şifrelenmeli mi? {#should-backups-be-encrypted}

Hassas kurtarma verileri uygun olduğunda şifrelenmelidir; ancak kurtarma parolasını veya anahtarını arızalanan VPS'nin dışında güvenle saklayın.

### Çoğaltma bir yedek midir? {#is-replication-a-backup}

Tek başına değildir. Çoğaltma, yanlışlıkla silmeyi, bozulmayı veya kötü amaçlı değişiklikleri de kopyalayabilir. Çoğaltma veya yedekte bekleyen sisteme ek olarak geçmişe ait sürümlendirilmiş yedekler tutun.

### VDSina VPS yedekleri sunuyor mu? {#does-vdsina-provide-vps-backups}

VDSina; elle ve zamanlanmış yedek kopyalarını, geri yükleme ve yedekten sunucu oluşturma işlevlerini, indirilebilir yedek imajlarını belgeliyor. Hizmet koşulları yedekleme sorumluluğunu yine müşteriye veriyor ve dönemsel geri yükleme testleri öneriyor.

### Geri yüklemeyi ne sıklıkta test etmeliyim? {#how-often-should-i-test-restores}

Belirlenmiş bir takvimle ve önemli yedekleme veya mimari değişikliklerinden sonra test edin. Yüksek değerli veya hızla değişen sistemlerde, ölçülen kurtarma sürecinin güvenilir kalmasını sağlayacak kadar sık test yapılmalıdır.

### RTO hedefim bir saatten kısaysa ne yapmalıyım? {#what-if-my-rto-is-under-one-hour}

Yalnızca yedeklemeye dayanan tasarım çok yavaş kalabilir. Tam kurtarma tatbikatının süresini ölçün. Ölçülen RTO hedefi karşılamıyorsa otomasyon, hazır kurtarma imajları, kısmen hazır bekleyen yedek sistem veya mimari değişiklikleri değerlendirin.
