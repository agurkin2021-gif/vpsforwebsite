---
title: "VPS güvenlik kontrol listesi"
description: "VPS güvenlik kontrol listesi: yönetici erişimini güçlendirin, açık hizmetleri güvenlik duvarıyla sınırlayın, yazılımları güncelleyin, gizli bilgileri koruyun, yedekleri doğrulayın ve erişiminizi kaybetmeden olay müdahalesine hazırlanın."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-guvenlik-kontrol-listesi"
---

VPS güvenlik kontrol listesi, internete açık ve kendi yönettiğiniz bir sunucu için önceliklendirilmiş bir güvenlik sıkılaştırma sürecidir. Amaç VPS'yi «%100 güvenli» yapmak değildir. Amaç gereksiz saldırı yüzeyini azaltmak, ayrıcalıklı erişimi korumak, yazılımları güncel tutmak, kurtarmayı mümkün kılmak ve güvenlik işlerinin bir sorumlusunun bulunduğunu doğrulamaktır.

Güvenli işlem sırası önemlidir: **önce kurtarma yolunu koruyun, ikinci bir yönetici oturumunu doğrulayın, dışarıya açık hizmetleri listeleyin; ardından SSH ve güvenlik duvarı kurallarını sıkılaştırın**.

Ekibinizde güncellemeler, güvenlik duvarı politikası, yedek doğrulama, izleme ve olayların sorumlusu yoksa önce yönetim modelini çözün: [Yönetilen ve yönetilmeyen VPS karşılaştırması]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Genel sunucu seçimi için [Web sitesi için VPS]({{< relref "_index.md" >}}) sayfasına bakın.

[Temel önlemler](#security-baseline-in-order) · [Kontrol aracı](#vps-security-baseline-checker) · [SSH](#harden-administrative-access) · [Güvenlik duvarı](#firewall-only-the-services-you-need) · [Güncellemeler](#patching-and-automatic-security-updates) · [Yedekler](#backups-are-a-security-control) · [Olay müdahalesi](#after-a-suspected-compromise) · [Sık sorulan sorular](#faq)

## Sırasıyla temel güvenlik önlemleri {#security-baseline-in-order}

İnternete açık tipik bir Linux VPS için:

1. **Sağlayıcı konsolu ve kurtarma erişimini kullanılabilir tutun.**
2. **Adı belirli, root olmayan bir yönetici kullanıcısı oluşturup test edin.**
3. **SSH anahtarıyla kimlik doğrulamayı ekleyin ve ikinci bir oturum açarak doğrulayın.**
4. **Dinleyen bütün hizmetleri ve açık portları listeleyin.**
5. **SSH, root ve parola politikasını yalnızca anahtarla erişim çalıştıktan sonra kısıtlayın.**
6. **Varsayılan olarak engelleyen bir güvenlik duvarı politikası uygulayın ve yalnızca gerekli portları açın.**
7. **Veritabanlarını, Redis'i ve dahili uygulama portlarını varsayılan olarak özel ağda tutun.**
8. **İşletim sistemi ve paket güvenlik güncellemelerini uygulayın; hizmet ve sunucu yeniden başlatmalarının sorumlusunu belirleyin.**
9. **Kontrol panellerini, CMS'leri, eklentileri, çalışma ortamlarını ve bağımlılıkları da güncel tutun.**
10. **Gizli bilgileri koruyun; kullanıcı ve veritabanı hesaplarına yalnızca gereken yetkileri verin.**
11. **Ek savunma katmanı olarak kaba kuvvet ve istek hızı sınırlama kontrolleri ekleyin.**
12. **Herkese açık web sitelerinde HTTPS kullanın ve yönetim arayüzlerini koruyun.**
13. **Bağımsız yedekler tutun ve geri yüklemeyi test edin.**
14. **Güvenlik ve kurtarma sorunlarını ortaya çıkarabilecek günlükleri ve uyarıları etkinleştirin.**
15. **Bir ihlal şüphesinden sonra yapılacakları tanımlayın.**
16. **Denetimi düzenli olarak tekrarlayın.**

Uzaktan erişimi, komutları anlamadan yapıştırarak sıkılaştırmayın. Yetkili yöneticinin erişimini kesen bir güvenlik değişikliği hizmet kesintisidir.

## VPS temel güvenlik kontrol aracı {#vps-security-baseline-checker}

Temel önlemlerdeki eksikleri belirlemek için bu aracı kullanın. Araç, sunucunun güvenli olduğunu belgelemez.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-security-checker">
  <div class="mb-6">
    <label for="sec-recovery" class="form-label">Sağlayıcı konsolu ve kurtarma yolu test edildi mi?</label>
    <select id="sec-recovery" class="form-input"><option value="no">Hayır / bilinmiyor</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-admin" class="form-label">Root olmayan, adı belirli yönetici hesabında SSH anahtarıyla giriş test edildi mi?</label>
    <select id="sec-admin" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-firewall" class="form-label">Güvenlik duvarı etkin mi ve yalnızca gerekli genel portlara izin veriliyor mu?</label>
    <select id="sec-firewall" class="form-input"><option value="no">Hayır / bilinmiyor</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-services" class="form-label">Dinleyen hizmetler ve açık portlar listelendi mi?</label>
    <select id="sec-services" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-updates" class="form-label">İşletim sistemi ve uygulama güvenlik güncellemelerinin sorumlusu ile yeniden başlatma süreci belirlendi mi?</label>
    <select id="sec-updates" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-backup" class="form-label">Bağımsız yedek mevcut mu ve geri yükleme test edildi mi?</label>
    <select id="sec-backup" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-logs" class="form-label">Güvenlik ve kurtarma sorunları, birinin takip ettiği günlük veya uyarılara yansıyor mu?</label>
    <select id="sec-logs" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-app" class="form-label">CMS, panel, çalışma ortamı ve bağımlılık güncellemelerinin sorumlusu var mı?</label>
    <select id="sec-app" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-owner" class="form-label">Güvenlik olaylarından sorumlu kişi veya ekip belirli mi?</label>
    <select id="sec-owner" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Temel güvenlik önlemlerini kontrol edin</button>
</form>
<p id="vps-security-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Yalnızca uygulanmış ve test edilmiş kontrolleri işaretleyin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-security-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var ids = [
      "sec-recovery",
      "sec-admin",
      "sec-firewall",
      "sec-services",
      "sec-updates",
      "sec-backup",
      "sec-logs",
      "sec-app",
      "sec-owner"
    ];

    var missing = ids.filter(function (id) {
      return document.getElementById(id).value !== "yes";
    });

    var critical = ["sec-recovery", "sec-admin", "sec-firewall", "sec-updates", "sec-backup", "sec-owner"];
    var criticalMissing = critical.filter(function (id) {
      return document.getElementById(id).value !== "yes";
    });

    var result;

    if (criticalMissing.length >= 2) {
      result = "KRİTİK EKSİKLER: ayrıcalıklı erişim, güvenlik duvarı/güncellemeler, kurtarma veya olay sorumluluğu tamamlanmamış. Bu VPS'nin canlı kullanım için temel güvenlik hazırlığını tamamlanmış saymayın.";
    } else if (missing.length > 0) {
      result = "TEMEL ÖNLEMLER EKSİK: ana kontroller mevcut, ancak çözülmemiş madde sayısı: " + missing.length + ". Bu maddeleri tamamlayın; yalnızca yapılandırma dosyalarını değil, kontrollerin çalıştığını da doğrulayın.";
    } else {
      result = "CANLI KULLANIM İÇİN TEMEL ÖNLEMLER HAZIR: listedeki temel kontroller uygulanmış ve test edilmiş. Bu, güvenlik garantisi değildir; güncellemelere, izlemeye, yedek geri yükleme testlerine ve düzenli denetimlere devam edin.";
    }

    document.getElementById("vps-security-result").textContent = result;
  });
});
</script>

## Erişimi değiştirmeden önce kurtarma yolunu koruyun {#keep-a-recovery-path-before-changing-access}

SSH'yi kısıtlamadan veya sıkı bir güvenlik duvarı politikası etkinleştirmeden önce hatalı bir kuraldan sonra erişimi kurtarabileceğinizi doğrulayın.

Sağlayıcının tarayıcı konsolu, VNC veya kurtarma arayüzü gibi normal ağ erişiminden bağımsız en az bir seçeneği kullanılabilir tutun.

Ardından:

1. adı belirli yönetici kullanıcısını oluşturun;
2. SSH açık anahtarını ekleyin;
3. **ikinci** bir terminal oturumu açın;
4. oturum açmayı ve sudo/yönetici yetkilerini doğrulayın;
5. yeni politikayı test ederken çalışan oturumu açık tutun;
6. ancak bundan sonra eski erişim yöntemlerini kısıtlayın.

Asıl güvenlik kontrolü «root erişimini olabildiğince çabuk kapatmak» değildir. **Riskli erişimi, erişim kilitlenmesine yol açmadan test edilmiş daha güvenli bir yolla değiştirmektir**.

İlk kurulum süreci [VPS üzerinde web sitesi yayınlama]({{< relref "how-to-host-a-website-on-vps.md" >}}) sayfasında anlatılır.

## Engellemeden önce dışarıya açık hizmetleri listeleyin {#inventory-exposed-services-before-blocking}

Hangi portların açık olduğunu tahmin etmeyin.

Linux'ta dinleyen soketleri şu tür araçlarla inceleyin:

```bash
sudo ss -lntup
```

Her dinleyen hizmet için şunlara karar verin:

- hizmetin çalışması gerekiyor mu?
- bütün ağ arayüzlerinde dinlemesi gerekiyor mu?
- herkese açık olması gerekiyor mu?
- yalnızca localhost'a veya özel ağa bağlanabilir mi?
- hangi kaynak ağlar erişebilmeli?
- güncellemelerinden ve günlüklerinden kim sorumlu?

Genel web sitesi portları genellikle şunları içerebilir:

- SSH ve yönetici erişimi;
- HTTP 80;
- HTTPS 443.

Bu, her sunucunun bu üçünü de bütün internete açması gerektiği anlamına **gelmez**.

Kullanılmayan hizmetleri yalnızca güvenlik duvarıyla gizlemek yerine kaldırın.

## Yönetici erişimini güçlendirin {#harden-administrative-access}

Ubuntu'nun OpenSSH belgeleri açık anahtarla kimlik doğrulamayı destekler ve Ed25519 gibi modern anahtar algoritmalarını önerir.

Temel bir yönetici erişim modeli şunları içerir:

- adı belirli yönetici hesabı;
- SSH anahtarıyla kimlik doğrulama;
- uygulanabildiğinde parola ifadesiyle korunan özel anahtar;
- yalnızca ihtiyaç duyan kullanıcılara sudo yetkisi;
- root olarak çalışmayan uygulamalar;
- daha güvenli erişim doğrulandıktan sonra doğrudan root ve parolalı SSH erişiminin kısıtlanması.

Daha yüksek güvence gerektiren ortamlarda OpenSSH, FIDO/U2F veya TOTP tabanlı iki faktörlü kimlik doğrulama gibi daha güçlü modelleri de destekler.

### Root girişi ve parola ile kimlik doğrulama {#root-login-and-password-authentication}

Anahtarla erişimi ve konsoldan kurtarmayı doğrulamadan bu seçenekleri gelişigüzel ayarlamayın.

Daha güvenli yol çalıştıktan sonra şunları gözden geçirin:

- `PermitRootLogin`;
- `PasswordAuthentication`;
- `AllowUsers` / `AllowGroups`;
- gerektiğinde boşta kalma ve oturum politikası.

Kesin politika ortama bağlıdır.

SSH'yi 22 numaralı porttan taşımak tarama trafiğini azaltabilir; ancak anahtarların, en az yetki ilkesinin, güvenlik duvarı politikasının ve güncel yazılımın yerine **geçmez**.

## Güvenlik duvarı: yalnızca gerekli hizmetler {#firewall-only-the-services-you-need}

Ubuntu'nun varsayılan sunucu güvenlik duvarı arayüzü UFW'dir.

Güvenli bir temel politika şu yaklaşımı izler:

- talep edilmemiş gelen trafiği varsayılan olarak engelleyin;
- gerçekten kullandığınız yönetici erişim yoluna izin verin;
- herkese açık web sunucusunda HTTP ve HTTPS'ye izin verin;
- veritabanlarını ve dahili hizmetleri özel tutun;
- IPv4 ve IPv6 davranışını inceleyin.

Kısıtlayıcı kuralları etkinleştirmeden önce SSH erişimini koruyun.

Örnek inceleme:

```bash
sudo ufw status verbose
```

Mimariniz farklıysa genel bir «22/80/443 portlarına izin ver» listesini kopyalamayın.

### Sağlayıcı güvenlik duvarı ve sunucu güvenlik duvarı {#provider-firewall-and-host-firewall}

Sağlayıcı veya ağ güvenlik duvarı, trafiği sanal makineye ulaşmadan engelleyebilir.

Sunucu güvenlik duvarı, konuk işletim sisteminin hangi trafiği kabul edeceğini kontrol eder.

İkisini birlikte kullanmak yararlı bir ek savunma katmanı sağlayabilir; ancak kurallar belgelenmeli ve birbiriyle çelişmemelidir.

## Veritabanlarını ve dahili hizmetleri varsayılan olarak özel tutun {#keep-databases-and-internal-services-private-by-default}

MySQL/MariaDB/PostgreSQL, Redis, dahili Node/Python uygulama portları veya kontrol soketlerini yalnızca hizmet dinliyor diye internete açmayın.

Şunları tercih edin:

- aynı sunucudaki hizmetler için localhost;
- çok sunuculu mimariler için özel ağ arayüzleri;
- uzaktan yönetim gerektiğinde kaynak IP kısıtlamaları;
- yönetim işlemleri için SSH, VPN veya bastion erişimi.

Veritabanı portunu yalnızca mimari açıkça gerektiriyorsa ve erişim güçlü biçimde kısıtlanmışsa internete açın.

## Yamalar ve otomatik güvenlik güncellemeleri {#patching-and-automatic-security-updates}

Desteklenen bir işletim sistemi bile yama sürecinin sorumlusu yoksa zamanla güncelliğini kaybeder.

Ubuntu Server, desteklenen kurulumlarda otomatik güvenlik güncellemeleri için varsayılan olarak `unattended-upgrades` kullanır.

Bu yararlıdır; ancak güvenlik süreci şu soruları da yanıtlamalıdır:

- hangi paket depoları kapsanıyor?
- üçüncü taraf paketler ve uygulamalar güncelleniyor mu?
- bir hizmetin yeniden başlatılması gerekiyor mu?
- sunucunun yeniden başlatılması gerekiyor mu?
- başarısız güncellemeleri kim kontrol ediyor?
- canlı hizmetler ne zaman güvenle yeniden başlatılabilir?

Ubuntu belgeleri, güncellenen kodun devreye girmesi için hizmetlerin ve bazen sunucunun yeniden başlatılmasının gerekebileceğini belirtir.

«Otomatik güncellemeler açık» ifadesini bütün yama yönetimi süreci olarak görmeyin.

## Fail2ban, CrowdSec ve istek hızı sınırlama {#fail2ban-crowdsec-and-rate-limiting}

Kaba kuvvet koruma araçları, tekrarlanan kötüye kullanım girişimlerini azaltabilir.

Bunlar **ek savunma katmanıdır**; temel kimlik doğrulama modeli değildir.

Bunları şu adımlardan sonra kullanın:

- ayrıcalıklı erişim korunduğunda;
- güçlü kimlik doğrulama kurulduğunda;
- dışarıya açık hizmetler bilinçli olarak açıldığında;
- günlükler mevcut olduğunda.

Bir engelleme aracı, zayıf parolayı, güncellenmemiş paneli veya dışarıya açık veritabanını güvenli hale getirmez.

## Uygulamalar ve veritabanları için en az yetki {#least-privilege-for-applications-and-databases}

En az yetki ilkesi bütün yazılım yığını için geçerlidir.

Şunları tercih edin:

- ayrı dağıtım ve yönetici kullanıcıları;
- ayrı uygulama kullanıcıları;
- her uygulama için ayrı veritabanı kullanıcıları;
- yalnızca gerekli veritabanı yetkileri;
- birbiriyle ilgisiz müşteri siteleri için ayrı kullanıcılar;
- yalnızca uygulamanın ihtiyaç duyduğu dizinlere yazma izni.

Şunlardan kaçının:

- web uygulamalarını root olarak çalıştırmak;
- veritabanının root veya yönetici hesabını uygulamalarla paylaşmak;
- izin sorunlarını `chmod 777` ile çözmeye çalışmak;
- daha güçlü yalıtım uygulanabiliyorken birbiriyle ilgisiz müşteri sitelerinde tek Unix kullanıcısı kullanmak.

Birden fazla siteyi yalıtmak için [Birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) sayfasına bakın.

## Gizli bilgileri ve erişim bilgilerini koruyun {#protect-secrets-and-credentials}

Canlı sistemin erişim bilgilerini şuralarda tutmayın:

- herkese açık Git depoları;
- web üzerinden erişilebilen belge kök dizinleri;
- hata ayıklama sayfaları;
- ekran görüntüleri, destek kayıtları ve sohbetler;
- kaçınılabildiğinde kabuk geçmişi;
- geniş kullanıcı gruplarınca okunabilen ortam değişkeni dosyaları.

Şunları koruyun:

- veritabanı parolaları;
- API anahtarları;
- SMTP erişim bilgileri;
- ödeme ve webhook gizli anahtarları;
- yedek depolama erişim bilgileri;
- panel ve yönetici erişim bilgileri;
- SSH özel anahtarları.

Çalışanlar veya yükleniciler ayrıldığında ya da ihlal şüphesinden sonra erişim bilgilerini yenileyin.

## Kontrol panelleri ve yönetim arayüzleri {#control-panels-and-admin-interfaces}

Kontrol paneli, ayrıcalıklı yetkilere sahip bir yönetim uygulamasıdır.

Şunları denetleyin:

- mevcut panel sürümü;
- panel yönetici hesapları;
- panel destekliyorsa iki faktörlü kimlik doğrulama (2FA);
- dışarıya açık yönetim portları ve ana makine adları;
- operasyon açısından uygulanabiliyorsa kaynak IP kısıtlamaları;
- eklenti ve uzantı envanteri;
- yedekleme ve geri yükleme davranışı;
- panel günlükleri ve başarısız giriş hareketleri.

Panel kurmanın VPS'yi güvenli veya yönetilen bir hizmet haline getirdiğini varsaymayın.

Panel seçimi için [Kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}), FASTPANEL seçeneği için [FASTPANEL ile VPS hosting]({{< relref "fastpanel-vps-hosting.md" >}}) sayfasına bakın.

## Uygulama, CMS ve çalışma ortamı güncellemeleri {#application-cms-and-runtime-updates}

Bütün yamaları uygulanmış bir işletim sistemi yine de güvenlik açığı olan bir uygulama barındırabilir.

Güvenlik sorumluluğu şunları da kapsamalıdır:

- PHP, Node, Python ve çalışma ortamları;
- uygulama çatısı;
- WordPress çekirdeği;
- eklentiler ve temalar;
- WooCommerce ve uzantıları;
- web sunucusu;
- kontrol paneli;
- kütüphaneler ve bağımlılıklar.

Artık güvenlik güncellemesi almayan, bakımı bırakılmış bileşenleri kaldırın.

WordPress'e özel işlemler için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}), işlem yapan mağazalar için [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) sayfasına bakın.

## HTTPS, bütün sunucuyu değil veri aktarımını korur {#https-protects-transport-not-the-whole-server}

Oturum açma veya hassas veri işleme özelliği olan canlı web sitelerinde HTTPS gereklidir; herkese açık siteler için de temel bir önlemdir.

İstemci ile sunucu arasında aktarılan veriyi korur.

Şunları düzeltmez:

- güvenlik açığı olan eklentiler;
- zayıf SSH güvenliği;
- internete açık veritabanları;
- sızdırılmış API anahtarları;
- güncelliğini yitirmiş paketler;
- güvenli olmayan dosya izinleri;
- eksik yedekler.

Sertifika yenilemeyi doğrulayın; süre dolumlarını ve başarısızlıkları izleyin.

## DDoS koruması, uygulama güvenliği değildir {#ddos-protection-is-not-application-security}

VDSina, şu anda Standard VPS için ücretsiz DDoS koruması sunduğunu belirtiyor.

Herkese açık soru-cevap sayfasında ücretsiz hizmetin **L3-L4 kanal/ağ katmanı saldırılarını** kapsadığı ve **SLA kapsamında olmadığı** belirtiliyor.

Bu koruma altyapı ve ağ katmanında yararlıdır; ancak şunların yerine geçmez:

- SSH güvenliğinin güçlendirilmesi;
- güvenlik duvarı politikası;
- web uygulaması güvenliği;
- uygulama katmanında istek hızı sınırlama;
- uygun durumlarda WAF ve bot kontrolleri;
- yamaların uygulanması;
- olay müdahalesi.

Ağ katmanındaki DDoS azaltımını, kapsamlı bir web sitesi güvenlik hizmeti olarak tanımlamayın.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS altyapısını inceleyin</a>
</p>
<p><small>Açıklama: Editörün VDSina ile profesyonel bir ilişkisi vardır. Bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Sağlayıcının DDoS koruması ve teknik desteği, konuk işletim sistemi ve uygulama güvenliğinin güçlendirilmesi veya yönetiminin yerine geçmez.</small></p>

## Yedekler bir güvenlik önlemidir {#backups-are-a-security-control}

Güvenlik; ihlal, fidye yazılımı, hatalı güncelleme ve yanlışlıkla silme sonrasında kurtarabilmeyi de kapsar.

En azından:

- çalışan VPS'nin dışında bir kopya tutun;
- yalnızca tek anlık görüntü veya sunucu imajına güvenmeyin;
- yedek erişim bilgilerini koruyun;
- mümkünse uygulamanın yedeklere erişmesini engelleyin;
- başarısız yedekleme görevlerini izleyin;
- geri yüklemeyi test edin;
- geri yükleme noktaları arasında ne kadar veri kaybedilebileceğini bilin.

CISA, kritik verilerin çevrimdışı ve şifrelenmiş yedeklerini tutmayı, bir felaket kurtarma senaryosunda geri yüklemeyi düzenli test etmeyi önerir.

RPO/RTO, saklama süresi ve yedekleme topolojisi tasarımı [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}}) sayfasında ayrıntılı ele alınır.

## Günlükler, uyarılar ve denetim izi {#logs-alerts-and-audit-trail}

Hiç izlemediğiniz güvenli bir yapılandırma sessizce bozulabilir.

En azından şunları izleyin:

- tekrarlanan SSH ve kimlik doğrulama hataları;
- beklenmedik yeni yönetici veya sudo kullanıcıları;
- başarısız panel girişleri;
- güvenlik duvarı değişiklikleri;
- yeni dinleyen portlar;
- hizmet çökmeleri ve yeniden başlatmalar;
- diskin dolması;
- uygulama veya web sunucusunda 5xx hata artışları;
- yedekleme hataları;
- sertifika yenileme hataları;
- kullanılıyorsa kötü amaçlı yazılım ve güvenlik aracı uyarıları.

Günlükleri, olayları incelemeye yetecek kadar uzun süre saklayın.

Eşik ve uyarı tasarımı [VPS izleme]({{< relref "vps-monitoring.md" >}}) sayfasında ayrıntılı ele alınır.

## Bir ihlal şüphesinden sonra {#after-a-suspected-compromise}

Ayrıcalıklı hesap veya root hesabının ele geçirildiğinden şüpheleniyorsanız, gelişigüzel bir «temizliği» sunucunun güvenli olduğunun kanıtı saymayın.

Daha güvenli bir müdahale sırası şöyledir:

1. etkilenen VPS'yi veya ağ yolunu **yalıtın**;
2. mümkünse ilgili günlük ve kanıtları koruyun;
3. hangi erişim bilgilerinin ve gizli bilgilerin açığa çıkmış olabileceğini belirleyin;
4. bunları temiz ve güvenilir bir sistemden yenileyin;
5. güvenilir olduğu bilinen uygulama ve veri geri yükleme noktasını belirleyin;
6. gerektiğinde sunucuyu güvenilir işletim sistemi ve yapılandırma kaynaklarından yeniden kurun;
7. ele geçirilmiş çalıştırılabilir dosyaları veya yapılandırmayı körlemesine geri getirmek yerine doğrulanmış verileri geri yükleyin;
8. canlı trafiği yeniden bağlamadan önce ilk erişimin nasıl elde edildiğini inceleyin.

CISA'nın olay müdahalesi rehberi yalıtımı, kanıt ve günlük incelemesini, doğrulanmış yedeklerden kurtarmayı vurgular.

İş açısından kritik bir sistemde yetkin bir olay müdahalesi veya güvenlik uzmanından destek alın.

## Kontrol listesini tekrarlayın {#repeat-the-checklist}

Güvenlik, yalnızca ilk kurulumda yapılan bir iş değildir.

Belirlenmiş aralıklarla şunları yeniden kontrol edin:

- yönetici kullanıcıları ve SSH anahtarları;
- sudo yetkileri;
- açık ve dinleyen portlar;
- güvenlik duvarı kuralları;
- desteklenmeyen paketler ve işletim sistemi sürümleri;
- bekleyen güvenlik güncellemeleri;
- kontrol paneli, CMS ve eklenti sürümleri;
- yedekleme başarısı ve geri yükleme testleri;
- sertifika süresi ve yenileme;
- günlükler ve uyarılar;
- kullanılmayan hesaplar ve hizmetler;
- açığa çıkan gizli bilgiler;
- olay sırasında ulaşılacak kişiler.

Büyük taşımalar, panel değişiklikleri, yeni hizmetler veya mimari değişikliklerden sonra da kontrol listesini yeniden uygulayın.

## Canlı kullanım için güvenlik kontrol listesi {#production-security-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| Kurtarma erişimi | sağlayıcı konsolu veya kurtarma yolu çalışıyor |
| Yönetici girişi | root olmayan, adı belirli yönetici ve test edilmiş anahtarla giriş var |
| SSH politikası | güvenli alternatif erişimden sonra root ve parola politikası bilinçli olarak ayarlandı |
| Hizmetler | dinleyen portlar listelendi ve gerekçelendirildi |
| Güvenlik duvarı | varsayılan engelleme ve asgari açıklık uygulanıyor; gerekli yönetim ve web erişimi test edildi |
| Dahili hizmetler | açık bir gereksinim olmadan veritabanı, önbellek ve uygulama portları internete açık değil |
| Yamalar | işletim sistemi ve uygulama güncelleme sorumluları belirli; yeniden başlatma süreci biliniyor |
| En az yetki | uygulama, veritabanı ve kullanıcılar yalnızca gerekli erişime sahip |
| Gizli bilgiler | herkese açık değil; web üzerinden veya geniş yetkilerle okunamıyor |
| Panel ve yönetim arayüzü | güncel; yönetici erişimi, 2FA ve kısıtlamalar incelendi |
| TLS | geçerli HTTPS ve yenileme yolu var |
| Kaba kuvvet kontrolleri | yararlı olduğunda ek savunma katmanı olarak kullanılıyor |
| Yedekler | bağımsız kopya ve geri yükleme testi var |
| Günlükler | kimlik doğrulama, yönetim, hizmet ve yedekleme hataları görülebiliyor |
| DDoS | sağlayıcı ve ağ korumasının kapsamı anlaşıldı |
| Olay müdahalesi | sorumlu, yalıtım ve temiz kurtarma yolu belirli |
| Düzenli denetim | sonraki inceleme tarihi ve süreci var |

## Teknik kaynaklar {#technical-references}

- Ubuntu Server — OpenSSH
- Ubuntu Server — Güvenlik duvarı ve UFW
- Ubuntu Server — Otomatik güncellemeler
- CISA — StopRansomware rehberi
- VDSina Standard VPS
- VDSina soru-cevap — DDoS korumasının kapsamı

## Sık sorulan sorular {#faq}

### Yeni bir VPS'de önce neyin güvenliğini sağlamalıyım? {#what-should-i-secure-first-on-a-new-vps}

Konsol ve kurtarma erişimini koruyun, root olmayan ve adı belirli bir yönetici oluşturup SSH anahtarıyla girişi test edin, dinleyen hizmetleri listeleyin; ardından SSH ve güvenlik duvarı politikasını sıkılaştırın. Erişimi doğrulamadan kilitlenmeye yol açabilecek birden fazla değişiklik yapmayın.

### SSH parola girişini kapatmalı mıyım? {#should-i-disable-ssh-password-login}

Tipik VPS yönetiminde anahtarla yönetici kimlik doğrulaması daha güçlüdür; ancak önce anahtarla girişi ve kurtarma konsolunu doğrulayın. Çalışan tek erişim yolunu kapatmayın.

### SSH portunu değiştirmeli miyim? {#should-i-change-the-ssh-port}

Tarayıcıların oluşturduğu trafiği ve günlük gürültüsünü azaltabilir; ancak temel bir güvenlik kontrolü değildir. Güçlü kimlik doğrulama, en az yetki, güvenlik duvarı politikası ve güncellemeler daha önemlidir.

### Fail2ban gerekli mi? {#do-i-need-fail2ban}

Her zaman değil; ancak tekrarlanan kötü amaçlı giriş denemelerine karşı yararlı bir ek savunma katmanı olabilir. SSH anahtarlarının, güncellemelerin veya hizmetleri doğru şekilde dışarıya açmanın yerine geçmez.

### VPS'de hangi portlar açık olmalı? {#which-ports-should-be-open-on-a-vps}

Yalnızca mimarinin gerektirdiği portlar. Herkese açık web sunucusunda genellikle HTTP, HTTPS ve kontrollü bir yönetim erişimi gerekir. Veritabanları ve dahili uygulama hizmetleri normalde özel kalmalıdır.

### Güvenlik duvarı, güvenlik açığı olan uygulamayı korur mu? {#does-a-firewall-protect-a-vulnerable-application}

Hayır. Güvenlik duvarı ağ erişimini sınırlar. İnternetten erişilebilen bir web uygulaması yine güvenli kod, desteklenen bağımlılıklar, güncellemeler ve uygulama düzeyinde kontroller gerektirir.

### Otomatik güvenlik güncellemeleri yeterli mi? {#are-automatic-security-updates-enough}

Hayır. Desteklenen işletim sistemi paketlerinde yardımcı olurlar; ancak üçüncü taraf uygulama ve bağımlılıklar ayrı güncellemeler gerektirebilir. Hizmet veya sunucu yeniden başlatmalarının da operasyon kapsamında yönetilmesi gerekebilir.

### HTTPS, VPS güvenliği için yeterli mi? {#is-https-enough-to-secure-a-vps}

Hayır. HTTPS veri aktarımını korur. Zayıf SSH güvenliğini, açık veritabanlarını, güvenlik açığı olan eklentileri, eski paketleri, sızdırılmış gizli bilgileri veya eksik yedekleri düzeltmez.

### VDSina DDoS koruması web sitesinin güvenliği için yeterli mi? {#is-vdsina-ddos-protection-enough-to-secure-the-website}

Hayır. VDSina şu anda ücretsiz DDoS koruması sunduğunu belirtiyor; herkese açık soru-cevap sayfası bu korumayı SLA olmadan L3-L4 olarak tanımlıyor. Konuk işletim sistemi, erişim, uygulama ve kurtarma güvenliğini yine sağlamalısınız.

### VPS'nin ele geçirildiğinden şüpheleniyorsam ne yapmalıyım? {#what-should-i-do-if-i-suspect-the-vps-was-compromised}

Sistemi yalıtın, ilgili kanıt ve günlükleri koruyun, açığa çıkan erişim bilgilerini temiz bir sistemden yenileyin. Ayrıcalıklı erişimin ele geçirildiğinden şüpheleniliyorsa güvenilir kaynaklardan yeniden kurmayı ve doğrulanmış yedekleri kullanmayı tercih edin. Kritik sistemlerde olay müdahalesi uzmanından destek alın.
