---
title: "Yönetilen ve yönetilmeyen VPS karşılaştırması"
description: "Yönetilen ve yönetilmeyen VPS karşılaştırması: güncelleme, güvenlik, yedekleme, izleme ve olay sorumluluklarını, gerçek maliyeti ve uygun yönetim modelini değerlendirin."
image: "images/home/vps-for-website-hero.webp"
slug: "yonetilen-ve-yonetilmeyen-vps-karsilastirmasi"
---

Yönetilen ve yönetilmeyen VPS karşılaştırması esas olarak **sunucu kurulduktan sonra işletimi kimin üstleneceği** kararıdır. Her iki modelde sanal makinenin CPU, RAM ve diski aynı olabilir. Değişen; işletim sistemi, güvenlik, web yazılımları, yedekler, izleme, sorun giderme ve kurtarma sorumluluğudur.

Genel satın alma kararı için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[Kısa yanıt](#quick-answer) · [Sorumluluk tablosu](#responsibility-matrix) · [Yönetim uygunluk aracı](#management-fit-checker) · [Gerçek maliyet](#compare-total-operating-cost-not-only-server-price) · [VDSina kapsamı](#how-the-vdsina-offer-fits-this-decision) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

| Seçim | Ne zaman daha uygun? | Temel risk |
|---|---|---|
| **Yönetilmeyen / kendi yönettiğiniz VPS** | siz veya ekibiniz Linux/Windows yönetebiliyor; işletim sistemini yamalayabiliyor, güvenliği sağlayabiliyor, yedekleri doğrulayabiliyor, servisleri izleyip olaylara müdahale edebiliyorsa | işletimi kimse üstlenmiyorsa düşük sunucu fiyatı pahalıya mal olabilir |
| **Yönetilen VPS** | tanımlı sunucu yönetim görevlerini sağlayıcı veya sözleşmeli yöneticinin üstlenmesini istiyorsanız ve kesinti maliyetliyse | “yönetilen” belirsiz olabilir; kapsam dışındaki işler size kalabilir |
| **Yönetilmeyen VPS + ücretli yönetim desteği** | root/kontrol ve düşük altyapı maliyeti istiyor, ancak her bakım veya olay işini kendiniz yapmak istemiyorsanız | ücretli müdahaleler arasında da açık sorumlu ve yanıt süreci gerekir |

En önemli satın alma kuralı basittir: **“yönetilen” kelimesini değil, görevlerin ve müdahale sınırlarının yazılı listesini satın alın.**

## Yönetilen hizmetin tek standart anlamı yoktur {#managed-does-not-have-one-standard-meaning}

“Yönetilen VPS” evrensel teknik özellik değildir. Sağlayıcılar bu etiketi çok farklı hizmet kapsamları için kullanabilir.

Bir yönetilen paket işletim sistemi güncellemelerini, güvenlik duvarını, izlemeyi ve geri yüklemeyi içerebilir. Diğeri yalnızca panel, kurulum yardımı ve destek taleplerini kapsayabilir. WordPress eklentileri, özel kod, veritabanı sorguları, API'ler veya iş mantığı gibi uygulama işleri yine kapsam dışında olabilir.

Fiyatları karşılaştırmadan önce şunları belirleyin:

- sağlayıcı neleri proaktif izliyor;
- neleri otomatik veya talep üzerine yamalıyor;
- hangi yedekleme görevleri oluşturuluyor;
- geri yükleme testi ve uygulaması dahil mi;
- hangi servisler kapsamda: Nginx/Apache, PHP, veritabanı, e-posta, Redis, Docker vb.;
- uygulama sorunlarını giderme dahil mi;
- acil müdahale 7/24 mü, yalnızca mesai saatlerinde mi;
- beklenen yanıt süresi ve üst desteğe aktarma yolu;
- hangi değişiklikler yönetim kapsamını geçersiz kılabilir veya sınırlayabilir;
- root erişimine izin veriliyor mu, özel değişikliklerden sonra ne oluyor.

Yönetilen VPS, yazılı kapsam gerçekten üstlenilmesini istediğiniz işlerle örtüştüğünde değerlidir.

## Ödeme yapmadan önce yönetim vaatlerini netleştirin {#decode-management-claims-before-paying}

Satış ifadelerini görevin üstlenildiğine kanıt olarak değil, doğrulama gerektiren başlıklar olarak ele alın.

| Paket sayfasındaki ifade | Yazılı olarak hâlâ gerekenler |
|---|---|
| **7/24 destek** | sunucuyu birinin proaktif izleyip izlemediği, destek talebi olmadan hangi olaylara müdahale edildiği, sanal sunucu işletim sistemi/uygulama işlerinin dahil olup olmadığı |
| **Tam yönetilen** | işletim sistemi, güvenlik duvarı, web yazılımları, veritabanı, yedekleme, izleme ve olay görevlerinin tam listesi; desteklenen yazılımlar; istisnalar |
| **Yedekler dahil** | sıklık, saklama, sunucu dışı konum, hata izleme, geri yükleme testi ve geri yüklemeyi kimin yaptığı |
| **İzleme dahil** | nelerin izlendiği, eşikler, uyarı alıcıları, kimin müdahale yetkisi olduğu ve mesai dışı yanıt |
| **Güvenlik yönetiliyor** | yama sıklığı, güvenlik duvarı sorumluluğu, SSH/RDP politikası, açık içeren paketlere ve ele geçirilmelere müdahale |
| **Taşıma dahil** | dosyalar, veritabanı, DNS, e-posta, son yazmalar, geri dönüş ve uygulamaya özgü işlerin kapsamı |
| **Kontrol paneli dahil** | yalnızca panel/lisans kapsamı; işletim sistemi yamaları, kurtarma, izleme ve olay sorumlularını ayrıca doğrulayın |

Sağlayıcı etiketi somut görev sorumluluğuna çeviremiyorsa paketleri karşılaştırırken belirsiz işleri hâlâ size ait sayın.

## Sorumluluk tablosu {#responsibility-matrix}

Bu tabloyu başlangıç modeli olarak kullanın; ardından “yönetilen” sütununu sağlayıcının gerçek yazılı kapsamıyla değiştirin.

| Görev | Yönetilmeyen VPS | Yönetilen VPS |
|---|---|---|
| Fiziksel donanım, güç, ağ, hipervizör | sağlayıcı | sağlayıcı |
| VPS hazırlama / işletim sistemi imajı | sağlayıcı genellikle kurulum araçlarını sunar | sağlayıcı, çoğunlukla kurulum yardımıyla |
| İşletim sistemi güncellemeleri ve güvenlik yamaları | **siz** | **yalnızca dahilse** sağlayıcı |
| Güvenlik duvarı / SSH / RDP sıkılaştırma | **siz** | **yalnızca dahilse** sağlayıcı |
| Web sunucusu ve çalışma ortamı yapılandırması | **siz** | desteklenen ortamlar için dahil olabilir |
| Veritabanı yönetimi | **siz** | kısmen dahil olabilir; sınırları doğrulayın |
| TLS sertifikası / yenilemeler | **siz veya otomasyonunuz/paneliniz** | dahil olabilir |
| Yedekleme görevi yapılandırması | **siz** | dahil olabilir |
| Geri yükleme testi | **siz** | sıklıkla ayrı sorumluluktur; doğrulayın |
| İzleme / uyarılar | **siz** | dahil olabilir |
| Kesintiye müdahale | **siz / yöneticiniz** | yalnızca yönetim kapsamı içinde sağlayıcı |
| WordPress/eklenti/özel kod sorunları | **siz / geliştirici** | çoğunlukla hariç veya sınırlı |
| Kaynak seçimi ve ölçeklendirme kararları | **siz** | çoğunlukla ortak karar; doğrulayın |
| DNS / e-posta / üçüncü taraf entegrasyonları | **açıkça kapsanmadıkça siz** | kapsam büyük ölçüde değişir |

Sağlayıcı görevi kimin üstlendiğini belirtmiyorsa doğrulanana kadar güvenle devredilmiş saymayın.

## Yönetim uygunluk aracı {#management-fit-checker}

Bu araç teknik yeteneğinizi puanlamaz. İşletim görevlerinin gerçek bir sorumlusu olup olmadığını kontrol eder.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="management-fit-checker-form">
  <div class="mb-6">
    <label for="mg-skill" class="form-label">Linux/Windows sunucu yönetimi becerisi</label>
    <select id="mg-skill" class="form-input">
      <option value="none">Az veya hiç yok</option>
      <option value="basic">Temel SSH/RDP ve panel kullanımı</option>
      <option value="confident">Canlı sunucuları güvenle yönetebiliyorum</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mg-patching" class="form-label">İşletim sistemi/güvenlik yamalarını üstlenen belirli kişi var</label>
    <select id="mg-patching" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-backup" class="form-label">Yedekleri ve geri yükleme testlerini üstlenen belirli kişi var</label>
    <select id="mg-backup" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-monitor" class="form-label">İzleme ve uyarılar yapılandırılmış, bir sorumlu müdahale ediyor</label>
    <select id="mg-monitor" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-incident" class="form-label">Acil sunucu olayına müdahale edebilecek biri var</label>
    <select id="mg-incident" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-critical" class="form-label">Bu site için kesinti ne kadar maliyetli?</label>
    <select id="mg-critical" class="form-input">
      <option value="low">Düşük — test/hobi/kritik olmayan</option>
      <option value="medium">Orta — kurumsal site</option>
      <option value="high">Yüksek — gelir/işletim siteye bağlı</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mg-custom" class="form-label">Root erişimi veya özel/desteklenmeyen yazılım ortamı gerekiyor mu?</label>
    <select id="mg-custom" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-adminhelp" class="form-label">Gerektiğinde sunucu yönetimi desteği alabilir veya sürekli destek anlaşması yapabilir misiniz?</label>
    <select id="mg-adminhelp" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Yönetim modelini değerlendirin</button>
</form>
<p id="management-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">İşi gerçekten kimin yapacağına göre yanıtlayın.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("management-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) {
      return document.getElementById(id).value;
    }

    var skill = val("mg-skill");
    var patching = val("mg-patching") === "yes";
    var backup = val("mg-backup") === "yes";
    var monitor = val("mg-monitor") === "yes";
    var incident = val("mg-incident") === "yes";
    var critical = val("mg-critical");
    var custom = val("mg-custom") === "yes";
    var adminHelp = val("mg-adminhelp") === "yes";

    var opsReady = patching && backup && monitor && incident;
    var result;

    if (skill === "confident" && opsReady) {
      result = "YÖNETİLMEYEN VPS UYGUN: temel işletim görevlerinin sorumlusu var. Yazılı işletim talimatlarını, geri yükleme testlerini ve izlemeyi sürdürün; yönetilmeyen VPS'te canlı ortam sorumluluğu ekibinizdedir.";
    } else if (custom && adminHelp) {
      result = "YÖNETİLMEYEN VPS + YÖNETİM DESTEĞİ UYGUN: kontrol ve özelleştirme gerekiyor; ancak bazı işletim görevleri kurum içinde karşılanmıyor. VPS'i yalnızca ücretli veya gerektiğinde çağrılan yöneticinin kapsamı eksik görevleri açıkça üstleniyorsa kendi yönetiminizde tutun. Etkisi yüksek yüklerde izleme ve olay müdahalesini de kapsama dahil edin.";
    } else if (critical === "low" && skill !== "none" && adminHelp) {
      result = "ÖĞRENME / KARMA MODEL UYGUN: dışarıdan yönetim desteğini bilinçli kullanırsanız kritik olmayan yükte yönetilmeyen VPS makul olabilir. Yama, yedekleme, izleme ve olay müdahalesi sorumluları belirlenmeden sunucuyu canlı kullanıma hazır saymayın.";
    } else {
      result = "YÖNETİLEN VPS UYGUN: önemli işletim görevlerinin şu anda sorumlusu yok. İş açısından kritik siteyi yönetilmeyen VPS'e koymadan önce yazılı kapsamı olan yönetilen hizmet seçin veya eşdeğer yönetim desteği ayarlayın.";
    }

    document.getElementById("management-fit-result").textContent = result;
  });
});
</script>

## Yönetilmeyen VPS gerçekte ne gerektirir? {#what-unmanaged-vps-really-requires}

Yönetilmeyen, “kötü destek” demek değildir. Ayrı anlaşma yoksa sağlayıcının altyapıyı sunduğu, sunucu yönetiminin sizde kaldığı anlamına gelir.

Canlı web sitesi için birinin şu işleri üstlenmesi gerekir:

- ilk güvenlik sıkılaştırması;
- SSH/RDP erişimi ve hesap güvenliği;
- işletim sistemi/çekirdek/paket güncellemeleri;
- güvenlik duvarı ve dışa açık servisler;
- web sunucusu, PHP/Node/Python ve veritabanı yapılandırması;
- TLS yenileme;
- günlük inceleme;
- gerektiğinde kötü amaçlı yazılım/kötüye kullanım müdahalesi;
- disk kapasitesi izleme;
- CPU/RAM/veritabanı izleme;
- yedekleme zamanlaması;
- geri yükleme testleri;
- olaylarda sorun giderme;
- başarısız güncelleme veya yapılandırma değişikliği sonrası kurtarma;
- uygulama dağıtım koordinasyonu.

Bu işlerin sorumlusu gösterilemiyorsa sunucu gerçekten “kendi yönetiminizde” değildir; yalnızca **yöneticisi olmayan yönetilmeyen sunucudur**.

### Uyarı işaretleri: yönetilmeyen model canlı ortam için uygun değil {#red-flags-unmanaged-is-a-poor-production-fit}

Şunlardan birkaçı geçerliyse iş açısından kritik siteyi henüz yönetilmeyen VPS'e koymayın:

- işletim sistemi/güvenlik yamalarını kimse üstlenmiyor;
- yedekler planlanmış ama geri yüklemeler hiç test edilmemiş;
- disk, CPU, bellek, veritabanı veya erişilebilirlik uyarılarını kimse izlemiyor;
- normal saatler dışında olaya müdahale edebilecek kişi yok;
- sunucuyu yalnızca bir geliştirici biliyor ve yazılı işletim talimatı yok;
- ekip, destek kapsamı dışındaki sanal sunucu işletim sistemi/uygulama sorunlarını sağlayıcının düzeltmesini bekliyor;
- kesinti satışları, müşteri erişimini veya iş süreçlerini durduracak.

Çözüm mutlaka “yönetilen hosting satın almak” değildir. Çözüm her işletim görevine belirli sorumlu atamaktır: ekibiniz, yönetilen hizmet sağlayıcısı veya sözleşmeli yönetici.

Kaynak seçimi için [web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) rehberini kullanın.

## Yönetilen VPS neleri kapsamalıdır? {#what-managed-vps-should-cover}

Yararlı yönetilen hizmet işletim işlerini azaltır; ancak sınırı açık olmalıdır.

Şunlara yazılı yanıt arayın:

- Sunucu proaktif izleniyor mu?
- İşletim sistemi/güvenlik güncellemeleri planlanıp uygulanıyor mu?
- Güvenlik duvarı ve sıkılaştırma işleri dahil mi?
- Hangi web/veritabanı ortamları destekleniyor?
- Yedekleme görevleri dahil mi?
- Geri yüklemeleri kim test ediyor?
- Olay sırasında geri yüklemeyi kim yapıyor?
- Servis hataları otomatik mi araştırılıyor, yalnızca destek talebi açınca mı?
- Uygulama düzeyinde sorun giderme dahil mi?
- WordPress/eklenti sorunları kapsamda mı?
- Veritabanı performans sorunları kapsamda mı?
- Özel paketler/Docker/servisler destekleniyor mu?
- Hangi yanıt süresi hedefleri geçerli?
- Mesai dışı olay müdahalesi dahil mi?
- Taşıma dahil mi?
- Paket dışında hangi işler ücretlendiriliyor?

Bu yanıtları “tam yönetilen”, “7/24 destek” veya kontrol panelinin varlığından çıkarmayın.

## Kontrol paneli yönetim hizmeti değildir {#control-panel-is-not-management}

Kontrol paneli rutin yönetimi kolaylaştırabilir:

- alan adları ve sanal konaklar;
- TLS sertifikaları;
- PHP sürümleri;
- veritabanları;
- kullanıcılar;
- posta kutuları;
- dosya yönetimi;
- zamanlanmış görevler.

Ancak panel şu işleri kendiliğinden yapmaz:

- işletim sisteminin ne zaman yamalanacağına karar vermek;
- yedekten kurtarmayı test etmek;
- disk dolması olayını araştırmak;
- bozuk veritabanı sorgusunu düzeltmek;
- ele geçirilmiş erişim bilgilerine müdahale etmek;
- gece saat 3'te siteyi izlemek;
- başarısız dağıtımdan kurtarmak.

Panel bir araçtır. Yönetim ise **sorumluluğu üstlenme ve müdahale hizmetidir**.

Panel destekli yönetim istiyorsanız [kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) rehberine bakın.

## Destek, sunucu yönetimi değildir {#support-is-not-server-administration}

Teknik destek ile sunucu yönetimi yalnızca sağlayıcının yazılı kapsamı böyle belirtiyorsa örtüşür.

Altyapı desteği makul olarak şu konularda yardımcı olabilir:

- başlamayan sanal makine;
- ağ erişilebilirliği;
- platform/kontrol paneli sorunları;
- depolama veya sanallaştırma sorunları;
- sağlayıcı tarafındaki olaylar.

Sunucu yönetimi şunları içerebilir:

- sanal sunucu işletim sistemini yamalama;
- Nginx/Apache yapılandırma;
- PHP/veritabanı servislerini düzeltme;
- SSH/güvenlik duvarını sıkılaştırma;
- günlükleri inceleme;
- yedekleri geri yükleme;
- özel yazılım sorunlarını giderme.

Bunlar farklı sorumluluklardır.

Bu ayrım, sitede bağlantı verilen sağlayıcı için önemlidir: VDSina Standard sayfası **kesintisiz teknik destek** sunarken, herkese açık soru-cevap bölümü **sunucu yönetimini ayrıca sipariş edilen ek hizmet** olarak açıklar. Bu nedenle “7/24 destek” ifadesini “tam yönetilen VPS” olarak yorumlamayın. Bu sağlayıcı sayfaları 13 Ekim 2026 tarihinde yeniden kontrol edildi; bunlara dayanarak karar vermeden önce güncel yönetim kapsamını ve ticari koşulları tekrar doğrulayın.

## Yalnızca sunucu fiyatını değil, toplam işletim maliyetini karşılaştırın {#compare-total-operating-cost-not-only-server-price}

VPS'in gerçek maliyeti sunucu faturasından daha geniştir.

Şu modeli kullanın:

**toplam işletim maliyeti = VPS + panel/lisanslar + yedekler + izleme + yönetici zamanı + ücretli destek/yönetim işleri + olay/kurtarma maliyeti**

Sunucu yönetimi zaten ekibinizin işinin parçasıysa yönetilmeyen VPS en ucuz seçenek olabilir.

Şu durumlarda pahalı seçenek olabilir:

- geliştirici rutin sunucu işlerinde üretken saatlerini kaybediyorsa;
- güvenlik güncellemeleri gecikiyorsa;
- yedekler var ama geri yüklemeler başarısız oluyorsa;
- disk veya veritabanı baskısını kimse fark etmiyorsa;
- kesinti, tek teknik kişinin uyanmasını bekliyorsa;
- acil çağrılan uzman sunucuyu olay sırasında öğrenmek zorunda kalıyorsa.

Yönetilen hizmet de kendiliğinden ucuz değildir. Yetkin işletim ekibiniz zaten varsa ve özel ortam gerekiyorsa, başka sağlayıcıya sınırlı yönetim için ödeme yapmak kayda değer işi azaltmadan maliyet ekleyebilir.

Yalnızca CPU/RAM'i değil, **sorumluluğu** fiyatlandırın.

Basit karşılaştırma tablosu:

| Maliyet / risk kalemi | Yönetilmeyen | Yönetilen / sözleşmeli yönetici |
|---|---|---|
| VPS altyapısı | aylık sunucu fiyatı | aylık sunucu fiyatı |
| Panel / lisanslar | kullanılıyorsa ekleyin | dahil olabilir veya olmayabilir |
| Yedek depolaması / araçlar | kullanılıyorsa ekleyin | dahil olup olmadığını doğrulayın |
| İzleme | sizin aracınız/zamanınız | dahil olup olmadığını doğrulayın |
| Rutin yönetim | personelinizin zamanı | yönetim/yönetici ücreti |
| Mesai dışı olaylar | nöbet maliyetiniz / gecikme riski | kapsam ve istisnaları doğrulayın |
| Geri yükleme / kurtarma | sizin sorumluluğunuz | uygulamanın dahil olup olmadığını doğrulayın |
| Uygulama hata ayıklama | geliştirici/yönetici maliyeti | çoğunlukla yine müşteri/geliştirici işi |

Doğru karşılaştırma “hangi aylık fatura düşük?” değil, “hangi model gerekli her işletim görevine kabul edilebilir toplam maliyet ve riskle sorumlu atıyor?” sorusudur.

## Güvenlik, yedekler ve olay müdahalesi {#security-backups-and-incident-response}

Bu üç alan, yönetim modelinin gerçekten işler olup olmadığını gösterir.

### Güvenlik {#security}

Şunları kimin üstlendiğini sorun:

- güvenlik güncellemeleri;
- güvenlik duvarı değişiklikleri;
- SSH/RDP politikası;
- güvenlik açığı içeren paketler;
- kötü amaçlı yazılım veya ele geçirilme incelemesi;
- erişim bilgilerinin yenilenmesi.

Somut güvenlik sıkılaştırma temeli için [VPS güvenlik kontrol listesi]({{< relref "vps-security-checklist.md" >}}) rehberini kullanın.

### Yedekler {#backups}

Ayrı ayrı sorun:

- yedekleme görevlerini kim oluşturuyor;
- kopyalar nerede saklanıyor;
- başarısız görevleri kim izliyor;
- geri yüklenebilirliği kim test ediyor;
- geri yüklemeyi kim yapıyor;
- geri yüklenen veriler ne kadar güncel olacak.

Sağlayıcının “yedekler dahil” demesi altı sorunun hepsini yanıtlamaz. RPO/RTO, saklama süresi, harici kopyalar ve kurtarma mimarisi için [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}}) rehberini kullanın.

### Olay müdahalesi {#incident-response}

Şunları tanımlayın:

- uyarıyı ne tetikliyor;
- kim alıyor;
- kimin müdahale yetkisi var;
- mesai dışında ne oluyor;
- neler sağlayıcı altyapısı, neler sizin sanal sunucu işletim sisteminiz/uygulamanız;
- üst desteğe aktarma yolu nedir.

Taşıma ve geri dönüş planı için [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberine bakın.

## Root erişimi ve değişiklik kontrolü {#root-access-and-change-control}

Yönetilmeyen VPS genellikle azami özgürlük sağlar: root/yönetici erişimi, özel paketler, özel güvenlik duvarı kuralları ve desteklenmeyen servisler sizin kararınızdır.

Yönetilen VPS de root erişimi sunabilir; ancak yönetim sınırları olabilir. Sağlayıcı desteklenmeyen paketlerin veya manuel değişikliklerin oluşturduğu sorunların sorumluluğunu reddedebilir.

Yönetilen hosting seçmeden önce sorun:

- Root/yönetici erişimim kalıyor mu?
- Hangi değişiklikler destekleniyor?
- Değişiklikler destek üzerinden mi yapılmalı?
- Sağlayıcı desteklenmeyen yapılandırmayı geri alabilir mi?
- Docker, özel çekirdek veya üçüncü taraf panel kurmak yönetim kapsamını değiştirir mi?
- Değişiklikleri kim belgeliyor?

Sınırsız kontrol temel gereksinimse, yönetilmeyen VPS ve yetkin yönetici; dar bir yazılım ortamını destekleyen yönetilen paketten daha uygun olabilir.

## Orta yol: yönetilmeyen VPS ve ücretli yönetici {#the-middle-ground-unmanaged-plus-paid-admin}

Seçim yalnızca “her şeyi kendin yap” veya “tam yönetilen hosting al” değildir.

Pratik bir orta yol:

- yönetilmeyen VPS;
- yararlı olduğu yerde kontrol paneli;
- otomatik izleme;
- bağımsız yedekler;
- belgelenmiş geri yükleme süreci;
- ücretli/isteğe bağlı yönetici;
- olaylarda üst desteğe başvurulacak kişi.

Rutin işletim biliniyor ancak taşıma, güvenlik sıkılaştırma, arıza veya karmaşık değişikliklerde uzman yardımına ihtiyaç duyuluyorsa bu model çalışır.

Sunucuyu kimse izlemiyor ve yöneticiye ancak uzun kesintiden sonra ulaşılıyorsa başarısız olur. Karma model de belirli bir işletim sorumlusu gerektirir.

## VDSina teklifi bu karara nasıl uyar? {#how-the-vdsina-offer-fits-this-decision}

Bağlantı verilen VDSina VPS, ayrıca sunucu yönetim kapsamı üzerinde anlaşmadıkça altyapı/kendi yönetiminiz modeli olarak değerlendirilmelidir.

Sağlayıcının herkese açık bilgilerinde şu anda şunlar görülür:

- Standard VPS'te kesintisiz teknik destek;
- sunucu kontrol araçları ve API;
- yedek imajı işlevi;
- müşteri sunucusu yönetimini ayrıca sipariş edilen hizmet olarak açıklayan ayrı soru-cevap kaydı.

Bu birleşim yararlıdır; ancak **tam yönetilen VPS ile aynı vaat değildir**.

Bu yolu seçerseniz satın almadan önce işletim sistemi güncellemelerini, güvenlik sıkılaştırmasını, izlemeyi, geri yükleme testlerini ve olayları kimin üstleneceğini belirleyin.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS yapılandırmalarını inceleyin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Bu sayfa VPS'i yönetilen hosting olarak sunmaz; siparişten önce güncel destek ve yönetim kapsamını sağlayıcıyla doğrulayın.</small></p>

### Sağlayıcı kaynakları {#provider-references}

- VDSina Standard VPS — güncel paket özellikleri ve teknik destek
- VDSina soru-cevap — sunucu yönetimi ve site taşıma hizmeti

## Yönetilen VPS için ödeme yapmadan önce sorulacaklar {#questions-to-ask-before-paying-for-managed-vps}

Satış etiketini kapsam olarak kabul etmeyin. Şu soruların yanıtını alın:

1. Destek talebi olmadan hangi somut görevler proaktif yapılıyor?
2. Hangi işletim sistemleri ve yazılım ortamları destekleniyor?
3. Güvenlik güncellemelerini kim, ne kadar hızlı uyguluyor?
4. Hangi izleme hizmetleri dahil?
5. Yedekleme görevleri dahil mi?
6. Geri yükleme testleri dahil mi?
7. Acil geri yüklemeleri kim yapıyor?
8. Hangi olaylara 7/24 müdahale ediliyor?
9. Hangi yanıt süresi hedefleri var?
10. Veritabanı kapsamda mı?
11. WordPress/uygulama/eklenti sorunları kapsamda mı?
12. E-posta yönetimi kapsamda mı?
13. Taşıma kapsamda mı?
14. Root/yönetici erişimim kalıyor mu?
15. Hangi özel değişiklikler desteklenmiyor?
16. Hangi görevler ayrı ücretlendiriliyor?

Sağlayıcı açık yanıt veremiyorsa paketi belirsiz görevler size kalıyormuş gibi fiyatlandırın.

## İş yükü ve iş riskine göre seçin {#choose-by-workload-and-business-risk}

### Test, hazırlık veya hobi sunucusu {#test-staging-or-hobby-server}

Arızanın ticari etkisi düşükse ve ortam işletimi öğrenmek için de kullanılıyorsa yönetilmeyen model makuldür.

### Kurumsal web sitesi {#business-website}

Yetkin sorumlu yamaları, yedekleri, izlemeyi ve olayları üstleniyorsa yönetilmeyen model iyi çalışabilir. Aksi halde yönetilen hizmet veya ücretli yönetim işletim riskini azaltır.

### WooCommerce, üyelik veya işlem odaklı site {#woocommerce-membership-or-transactional-website}

Atlanan yamanın, başarısız geri yüklemenin veya uzun kesintinin maliyeti aylık fiyat farkını hızla aşabilir. Ekip zaten sunucu işletmiyorsa desteğin uygulama işletimini üstleneceğini ummak yerine tanımlı yönetilen hizmet/yönetici desteğini tercih edin.

### Birden fazla müşteri sitesi {#multiple-client-websites}

Tüm sitelerdeki olayları kimin üstlendiğini ve tek sunucu arızasının birden fazla müşteriyi etkileyip etkilemediğini sorun. Sistem yönetimi yetkinliği olan ajans yönetilmeyen kontrolü tercih edebilir; işletim personeli olmayan ajans gerçek bir yönetim ve üst desteğe aktarma modeli gerektirir.

### Özel uygulama / alışılmadık yazılım ortamı {#custom-application--unusual-stack}

Yönetilmeyen model çoğunlukla daha fazla özgürlük verir; ancak yalnızca ekip kurduğu yazılımları işletebiliyorsa. Yönetilen paket desteklenmeyen çalışma ortamlarını, konteynerleri veya özel servisleri kapsam dışında bırakabilir.

## Sık sorulan sorular {#faq}

### Yönetilmeyen VPS ile kendi yönettiğiniz VPS aynı mı? {#is-unmanaged-vps-the-same-as-self-managed-vps}

Genellikle evet. İki terim de ayrı hizmet aksini belirtmedikçe sanal makine içindeki yönetimin çoğundan müşterinin sorumlu olduğunu anlatır.

### Yönetilmeyen VPS teknik destek içerir mi? {#does-unmanaged-vps-include-technical-support}

İçerebilir. Altyapı ve hesap desteği yine mevcut olabilir. Ayrım, teknik desteğin işletim sisteminizi, güvenliğinizi, yedeklerinizi, web yazılımlarınızı veya uygulamanızı kendiliğinden üstlenmemesidir.

### Kontrol paneli VPS'i yönetilen hizmete dönüştürür mü? {#does-a-control-panel-make-a-vps-managed}

Hayır. Panel birçok işi kolaylaştırır; ancak güncellemeleri, güvenliği, yedekleri, izlemeyi ve olay müdahalesini yine birinin üstlenmesi gerekir.

### Yönetilen VPS daha güvenli mi? {#is-managed-vps-more-secure}

Kendiliğinden değil. Yetkin yöneticiler sunucuyu gerçekten yamalıyor, sıkılaştırıyor ve izliyorsa işletim riskini azaltabilir. Güvenlik etikete değil, gerçek yönetim kapsamına ve uygulamasına bağlıdır.

### Yönetilen VPS her zaman daha mı pahalı? {#is-managed-vps-always-more-expensive}

Aylık fatura genellikle yüksektir; ancak değerli yönetici zamanını tasarruf ettiriyor veya pahalı olayları önlüyorsa toplam işletim maliyeti daha düşük olabilir. Zamanı, araçları, yedekleme/izleme maliyetlerini ve kurtarma riskini karşılaştırın.

### Yönetilen VPS'te root erişimi kullanabilir miyim? {#can-i-use-root-access-on-a-managed-vps}

Bazen. Politika değişir. Root/yönetici erişiminin kalıp kalmadığını ve özel değişikliklerin sağlayıcının yönetim sorumluluğunu azaltıp kaldırmadığını sorun.

### Yönetilmeyen VPS'i kim seçmeli? {#who-should-choose-unmanaged-vps}

Sunucu güncellemelerini, güvenlik sıkılaştırmasını, yedekleri, geri yükleme testlerini, izlemeyi ve olayları güvenilir biçimde üstlenebilen; yazılım ortamı üzerinde tam kontrole değer veren kullanıcı veya ekipler.

### Yönetilen VPS'i kim seçmeli? {#who-should-choose-managed-vps}

Canlı sunucuyu kendileri sürdürmek için zamanı, becerisi veya nöbet kapasitesi olmadığından tanımlı işletim hizmeti gerektiren ekipler.

### 7/24 destek, yönetilen VPS ile aynı mı? {#is-247-support-the-same-as-managed-vps}

Hayır. Sağlayıcı 7/24 teknik destek sunarken sunucu yönetimi ayrı hizmet olarak kalabilir. Yazılı kapsamı okuyun.
