---
title: "VPS üzerinde web sitesi yayınlama"
description: "VPS üzerinde web sitesi yayınlama: kurulum yolunu seçin, erişimi güvenli hale getirin, yazılımları kurun, alan adını ve HTTPS'i bağlayıp canlı kullanıma hazırlığı doğrulayın."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-uzerinde-web-sitesi-yayinlama"
---

VPS üzerinde web sitesi yayınlama yöntemi kurduğunuz uygulamaya bağlıdır. Statik site web sunucusu ve DNS gerektirir. WordPress veya başka PHP CMS'i ayrıca PHP ve veritabanı ister. Node.js veya Python uygulaması genellikle ters proxy arkasında çalışır. Bu bileşenleri temiz VPS'te manuel kurabilir veya tarayıcıdan yönetmek için kontrol paneli kullanabilirsiniz.

Bu rehber **yeni VPS'ten yayındaki web sitesine** uzanan süreci ele alır. Canlı verisi olan mevcut siteyi taşıyorsanız geçiş ve geri dönüş için [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberini kullanın.

Genel satın alma kararı için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[Hızlı sıra](#quick-deployment-sequence) · [Yol seçimi](#choose-manual-panel-or-managed) · [Kurulum aracı](#deployment-path-checker) · [Manuel yol](#manual--no-control-panel-path) · [DNS](#point-the-domain-to-the-vps) · [Canlı ortam kontrol listesi](#production-acceptance-checklist) · [Sık sorulan sorular](#faq)

## Hızlı kurulum sırası {#quick-deployment-sequence}

Güvenilir ilk kurulum şu sırayı izler:

1. **VPS'i ve kaynaklarını seçin.**
2. **Manuel, panelli veya yönetilen modeli seçin.**
3. **Temiz işletim sistemi veya sağlayıcının güncel panel imajını kurun.**
4. **İlk erişimi güvenli hale getirip root olmayan yönetici yolu oluşturun.**
5. **İşletim sistemini güncelleyin.**
6. **Yalnızca uygulamanın gerektirdiği web yazılımlarını kurun.**
7. **Mümkünse genel DNS geçişinden önce siteyi/uygulamayı yapılandırın.**
8. **Dosyaları/kodu dağıtıp sahipliği, gizli bilgileri ve veritabanı erişimini yapılandırın.**
9. **SSH ve gerekli HTTP/HTTPS erişimini koruyarak güvenlik duvarını sınırlandırın.**
10. **Genel DNS'ten önce hedefi test edin.**
11. **Alan adını VPS'e yönlendirin.**
12. **Ana makine adı sunucuya ulaştıktan sonra HTTPS'i etkinleştirin.**
13. **Cron/işçi süreçlerini, günlükleri, yedekleri ve harici izlemeyi doğrulayın.**
14. **Bir kez yeniden başlatıp gerekli tüm servislerin otomatik döndüğünü doğrulayın.**
15. **Ancak bundan sonra kurulumu canlı kullanıma hazır sayın.**

Genel VPS rehberinde yer alıyor diye PHP, MySQL, e-posta veya kontrol paneli kurmayın. Sitenin gerçekten gerektirdiği bileşenleri kurun.

## Manuel, panelli veya yönetilen modeli seçin {#choose-manual-panel-or-managed}

Üç ayrı işletim yolu vardır.

### Manuel / kontrol panelsiz {#manual--no-control-panel}

Temiz Linux VPS seçip yazılım ortamını SSH üzerinden yönetin.

Şu durumlarda uygundur:

- uygulamanın yazılım ortamını biliyorsanız;
- çalışan servisleri asgari tutmak istiyorsanız;
- özel Nginx/Apache/çalışma ortamı yapılandırması gerekiyorsa;
- betikler, Git veya kodla altyapı yönetimi kullanıyorsanız;
- geleneksel hosting hesabı arayüzü gerekmiyorsa.

**Kontrol panelsiz VPS** kurulumu da bu rehberdeki manuel yolda ele alınır.

### Kontrol paneli {#control-panel}

Tarayıcıdan site, alan adı, PHP, veritabanı, e-posta veya kullanıcı yönetimi kayda değer tekrarlayan işi azaltıyorsa hosting paneli kullanın.

[Kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) rehberine bakın. FASTPANEL'i zaten seçtiyseniz [FASTPANEL ile VPS hosting]({{< relref "fastpanel-vps-hosting.md" >}}) rehberini kullanın.

### Yönetilen hizmet {#managed-administration}

Panel ve yönetim farklıdır. Sizin tarafınızda yamaları, güvenliği, yedekleri, izlemeyi ve olayları kimse üstlenmiyorsa yayına çıkmadan önce bunu belirleyin.

[Yönetilen ve yönetilmeyen VPS karşılaştırmasına]({{< relref "managed-vs-unmanaged-vps.md" >}}) bakın.

## Kurulum yolu aracı {#deployment-path-checker}

Bu araç araştırılacak yazılım yolunu belirler. Uygulama belgelerinin yerini tutmaz.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="deployment-path-checker-form">
  <div class="mb-6">
    <label for="deploy-type" class="form-label">Web sitesi / uygulama türü</label>
    <select id="deploy-type" class="form-input">
      <option value="static">Statik HTML / oluşturulmuş statik site</option>
      <option value="php">WordPress / PHP CMS</option>
      <option value="app">Node.js / Python / özel uygulama</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="deploy-panel" class="form-label">Hosting kontrol paneli tercih ediyor musunuz?</label>
    <select id="deploy-panel" class="form-input"><option value="no">Hayır / manuel</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-db" class="form-label">Uygulama yerel veritabanı gerektiriyor mu?</label>
    <select id="deploy-db" class="form-input"><option value="no">Hayır</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-mail" class="form-label">Posta kutuları aynı VPS'te barındırılacak mı?</label>
    <select id="deploy-mail" class="form-input"><option value="no">Hayır / harici e-posta</option><option value="yes">Evet</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-sites" class="form-label">Etkin web sitesi sayısı</label>
    <select id="deploy-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Kurulum yolunu seçin</button>
</form>
<p id="deployment-path-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">İş yükünü ve yönetim tercihini seçin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("deployment-path-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var type = document.getElementById("deploy-type").value;
    var panel = document.getElementById("deploy-panel").value === "yes";
    var db = document.getElementById("deploy-db").value === "yes";
    var mail = document.getElementById("deploy-mail").value === "yes";
    var sites = document.getElementById("deploy-sites").value;

    var result;

    if (panel) {
      result = "KONTROL PANELİ YOLU: son işletim sistemi imajından önce paneli seçin. İşletim sistemi uyumunu, panel yükünü, kullanıcı/site yalıtımını, e-posta/DNS ihtiyaçlarını, yedekleri ve yönetim sorumluluğunu doğrulayın.";
    } else if (type === "static" && !db && !mail) {
      result = "STATİK MANUEL YOL: temiz Linux + SSH + Nginx veya Apache + site dosyaları + DNS + HTTPS. Site gerçekten gerektirmedikçe PHP veya veritabanı kurmayın.";
    } else if (type === "php") {
      result = "PHP / WORDPRESS MANUEL YOL: Linux + SSH + Nginx/Apache + PHP-FPM + gerekiyorsa veritabanı + DNS + HTTPS. PHP süreçleri ve veritabanı için RAM ayırın.";
    } else if (type === "app") {
      result = "UYGULAMA + TERS PROXY YOLU: uygulamayı genellikle localhost üzerinde, kendine ait root olmayan servis/süreç yöneticisi altında çalıştırın. Ardından genel ana makine adı ve HTTPS için önüne Nginx/Apache koyun.";
    } else {
      result = "ÖZEL MANUEL YOL: uygulamanın belgelenmiş çalışma ortamından başlayıp yalnızca gerekli servisleri kurun.";
    }

    if (sites === "many") {
      result += " 6+ site için açıkça siteye özel kullanıcı/izinler ve toplam iş yükü planı ekleyin.";
    }
    if (mail) {
      result += " Yerel e-posta; SMTP/IMAP, DNS itibarı, depolama, yedekleme ve güvenlik işi ekler. Yönetilen harici e-postanın daha basit olup olmadığını yeniden değerlendirin.";
    }

    document.getElementById("deployment-path-result").textContent = result;
  });
});
</script>

## Ön gereksinimler {#prerequisites}

Sunucuda işleme başlamadan önce şunlar hazır olsun:

- iş yüküne göre boyutlandırılmış VPS;
- sunucunun IP adresi;
- SSH erişim bilgileri veya anahtar erişimi;
- çalışan sağlayıcı konsolu/VNC/kurtarma yolu;
- kayıtlı alan adı ve DNS erişimi;
- site dosyaları veya uygulama deposu;
- gerekli çalışma ortamı sürümleri;
- veritabanı gereksinimleri;
- gizli bilgiler/ortam değişkenleri için plan;
- yedek konumu;
- site erişilebilirliğini dışarıdan test etme yöntemi.

Kaynak ihtiyacı hâlâ belirsizse kurulumdan önce [web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) rehberini kullanın.

VDSina'nın mevcut Standard VPS sayfası; Ubuntu 26.04/24.04/22.04/20.04, Debian 13/12/11/10, AlmaLinux, Rocky, CentOS, Oracle Linux ve ArchLinux dahil sade işletim sistemi şablonlarını listeler. Bu rehber, güncel web sunucusu belgeleri ve paket akışı kolay takip edildiği için Ubuntu/Debian tarzı örnekler kullanır. Mimari, farklı paket/servis komutlarıyla diğer desteklenen Linux dağıtımlarına da uygulanır.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Web sitesi için VPS seçin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Sunucu kaynaklarını ve yönetim modelini komisyona değil, iş yüküne göre seçin.</small></p>

## İşletim sistemini seçin {#choose-the-operating-system}

Manuel web sunucusu için şu özelliklere sahip işletim sistemi seçin:

- uygulama/çalışma ortamı tarafından destekleniyor;
- bakımı devam ediyor;
- yöneticiniz biliyor;
- web yazılımları için güncel paket ve belgeleri var;
- sonradan panel kullanırsanız onun gereksinimine uyuyor.

İşletim sistemini yalnızca en yeni olduğu için seçmeyin. Uygulama uyumu ve yöneticinin aşinalığı daha önemlidir.

Basit güncel Linux örneği için Ubuntu 24.04 LTS veya Debian 12 makul belge hedefleridir. Uygulama üreticisi başka desteklenen dağıtım belirtiyorsa o gereksinimi izleyin.

## İlk SSH erişimini güvenli hale getirin {#secure-first-ssh-access}

Yeni VPS yönetici erişimi verir; ancak canlı ortam işleri sürekli root olarak yapılmamalıdır.

Güvenli ilk erişim sırası:

1. VPS sağlayıcısının verdiği erişim bilgileri/anahtarla bağlanın;
2. sunucu/IP'nin oluşturmak istediğiniz sunucu olduğunu doğrulayın;
3. sağlayıcı konsolu/VNC/kurtarma yolunu çalışır tutun;
4. kişisel yönetici kullanıcısı oluşturun;
5. yalnızca gerekli sudo/yönetici haklarını verin;
6. mümkünse SSH anahtarıyla kimlik doğrulama ekleyin;
7. ilk erişim yöntemini kapatmadan veya sınırlamadan **önce** ikinci oturumda yeni girişi doğrulayın.

Ubuntu/Debian örneği:

```bash
ssh root@SERVER_IP
adduser deploy
usermod -aG sudo deploy
```

Sunucuyu “sıkılaştırırken” çalışan tek yönetici yolunu kilitlemeyin.

Ayrıntılı SSH/güvenlik duvarı sıkılaştırması [VPS güvenlik kontrol listesinde]({{< relref "vps-security-checklist.md" >}}) ele alınır; bu rehber yalnızca kurulum için gereken temeli içerir.

## Yazılımları kurmadan önce sunucuyu güncelleyin {#update-the-server-before-installing-the-stack}

Ubuntu/Debian üzerinde:

```bash
sudo apt update
sudo apt upgrade -y
```

Güncelleme gerektiriyorsa yeniden başlatın, ardından tekrar bağlanabildiğinizi doğrulayın.

Güvenlik güncellemelerini site herkese açılana kadar ertelemeyin.

## Manuel / kontrol panelsiz yol {#manual--no-control-panel-path}

Manuel VPS yalnızca uygulamanın gerektirdiği servisleri içermelidir.

Yaygın seçenekler:

### Statik web sitesi {#static-website}

Gerekenler:

- Nginx veya Apache;
- web sitesi dosyaları;
- DNS;
- HTTPS.

Kendiliğinden gerekmeyenler:

- PHP;
- MySQL/MariaDB/PostgreSQL;
- yerel e-posta sunucusu.

### PHP / WordPress sitesi {#php--wordpress-website}

Genellikle gerekenler:

- Nginx veya Apache;
- PHP-FPM / PHP modülleri;
- veritabanı;
- site dosyaları/yüklemeler;
- DNS;
- HTTPS.

WordPress kaynak davranışı için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberini kullanın.

### Node.js / Python / özel uygulama {#nodejs--python--custom-application}

Genellikle:

- uygulama çalışma ortamı;
- uygulamaya özel, root olmayan kullanıcı;
- süreç yöneticisi/systemd servisi;
- mümkünse localhost/özel sokete bağlı uygulama;
- Nginx/Apache ters proxy;
- yalnızca gerekiyorsa veritabanı;
- DNS;
- HTTPS.

Canlı ortam mimarisi olarak geliştirme sunucusunu doğrudan genel internete açmayın.

## Web sunucusunu kurun {#install-the-web-server}

Ubuntu'nun güncel sunucu belgeleri hem Nginx'i hem Apache'yi destekler. Hiçbiri her durumda “daha iyi” değildir.

Nginx örneği için:

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

Ağ/güvenlik duvarı kuralları HTTP'ye izin veriyorsa bu aşamada sunucu IP'si varsayılan Nginx sayfasını döndürmelidir.

Uygulama, ekip veya mevcut yapılandırma Apache'ye daha uygunsa Apache kullanın.

## Site ana makine adını yapılandırın {#configure-the-website-hostname}

DNS ve web sunucusu yapılandırması aynı işin iki parçasıdır.

DNS sağlayıcısı ana makine adını VPS'e yönlendirmeli **ve** web sunucusu bu ada hangi sitenin yanıt vereceğini bilmelidir.

Nginx'te alan adı için sunucu bloğu oluşturun. Temel yapı:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name example.com www.example.com;
    root /var/www/example.com/public;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Ubuntu/Debian'da siteye özel yapılandırmalar çoğunlukla şu dizinlerde bulunur:

- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

Değişikliklerden sonra:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Yeniden yüklemeden önce daima yapılandırma sözdizimini test edin.

Ters proxy uygulamasında sunucu bloğu istekleri yerel uygulama portuna veya soketine iletir.

## Dosyaları veya uygulama kodunu dağıtın {#deploy-files-or-application-code}

Tekrarlanabilir dağıtım yöntemi seçin.

### SFTP/SCP {#sftpscp}

Şunlar için uygundur:

- küçük siteler;
- seyrek manuel dağıtımlar;
- ilk kez kurulan basit projeler.

Risk: canlı dizinin kaynak deposundan uzaklaşması kolaydır.

### SSH üzerinden rsync {#rsync-over-ssh}

Tekrarlanabilir dosya eşitlemesi ve verimli artımlı güncellemeler için yararlıdır.

### Git tabanlı dağıtım {#git-based-deployment}

Canlı sürümlerin depodaki commit'lerle eşleşmesi gerektiğinde yararlıdır.

### CI/CD {#cicd}

Dağıtım, otomatik derleme/test/yayın adımlarını haklı çıkaracak kadar sıksa yararlıdır.

Hangi yöntemi kullanırsanız kullanın:

- iş gerçekten gerektirmedikçe root olarak dağıtmayın;
- uygulama dosyalarının sahipliğini uygun dağıtım/uygulama kullanıcısında tutun;
- web sunucusuna yalnızca gereken erişimi verin;
- gizli bilgileri herkese açık site kök dizinlerinin dışında tutun;
- herkese yazma iznini kestirme yol olarak kullanmayın.

## PHP / WordPress yolu {#php--wordpress-path}

Ubuntu/Debian üzerinde PHP sitesi için güncel desteklenen PHP-FPM paketlerini ve uygulamanın gerekli eklentilerini kurun.

Tipik mimari:

**tarayıcı -> Nginx/Apache -> PHP-FPM -> veritabanı**

Başka CMS'ten rastgele eklenti listesi kopyalamayın. Uygulamanın gerçekten gerektirdiklerini kurun.

WordPress için:

- veritabanı ve ona özel kullanıcı oluşturun;
- PHP yükleme/bellek/çalışma süresi sınırlarını ölçülen ihtiyaca göre yapılandırın;
- `wp-config.php` içindeki gizli bilgileri koruyun;
- site ana makine adını yapılandırın;
- HTTPS'i etkinleştirin;
- wp-cron/arka plan görevlerini doğrulayın;
- iş yüküne göre önbellekleme ekleyin.

Kaynak seçimi ve performans için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberini kullanın.

## Node.js / Python / özel uygulama yolu {#nodejs--python--custom-app-path}

Geliştirme komutunu terminalde manuel çalıştırıp bunu canlı ortam saymayın.

Şunları kullanın:

- uygulamaya özel kullanıcı;
- kısıtlı izinlere sahip ortam/yapılandırma dosyası;
- systemd veya uygun canlı ortam süreç yöneticisi;
- hata/yeniden başlatma sonrasında otomatik başlatma;
- yerel/özel uygulama dinleyicisi;
- Nginx/Apache ters proxy;
- uygulama günlükleri;
- sağlık kontrolleri.

Tipik akış:

**tarayıcı -> HTTPS/Nginx -> 127.0.0.1:PORT üzerindeki uygulama -> veritabanı/harici servisler**

Framework'ün kendi canlı ortam dağıtım rehberini doğrulayın.

## Veritabanını yalnızca gerektiğinde kurun {#database-install-only-when-required}

Statik site veritabanı gerektirmez.

Veritabanı isteyen dinamik uygulamada:

- desteklenen veritabanı motorunu kurun;
- ayrı veritabanı oluşturun;
- uygulamaya özel kullanıcı oluşturun;
- yalnızca gereken yetkileri verin;
- erişim bilgilerini web kök dizininin dışında tutun;
- bunu gerektiren somut ve güvenli mimari yoksa veritabanı portunu herkese açmayın;
- veritabanını yedekleme ve izleme planına dahil edin.

Web sunucusu neredeyse boşta olsa bile asıl VPS darboğazı veritabanı işi olabilir.

## Dosya sahipliği, izinler ve gizli bilgiler {#file-ownership-permissions-and-secrets}

İki yaygın hatadan kaçının:

1. siteyi root olarak çalıştırmak;
2. izin hatalarını “düzeltmek” için uygulama dizinlerini herkese yazılabilir yapmak.

Bunun yerine:

- dağıtım/uygulama kullanıcısı kullanın;
- hangi sürecin okuma, hangisinin yazma erişimi istediğini anlayın;
- yükleme/önbellek dizinlerine yalnızca gerekli yazma erişimini verin;
- ortam dosyalarını ve erişim bilgilerini koruyun;
- canlı ortam gizli bilgilerini Git'e kaydetmeyin;
- özel anahtarları herkese açık site kök dizinlerinin dışında tutun.

Kesin sahiplik uygulamaya ve web sunucusu modeline bağlıdır; evrensel `chmod 777` tarifini kopyalamak yerine uygulama belgelerini kullanın.

## Genel DNS'ten önce test edin {#test-before-public-dns}

DNS'i uygulamanın ilk gerçek testi haline getirmeyin.

Genel geçişten önce mümkünse şu yöntemlerden biriyle yeni sunucuyu doğrulayın:

- basit varsayılan/statik kontrol için sunucu IP'sine erişin;
- `example.com` yalnızca sizin bilgisayarınızda yeni VPS'e çözümlensin diye yerel hosts dosyasını kullanın;
- yanlışlıkla dizine giren kopyaya dönüşmesi engellenmiş özel/test ana makine adı kullanın;
- uygulamayı canlıda kullanılacak aynı Nginx/Apache ana makine adı yapılandırması üzerinden test edin.

Ana sayfadan fazlasını kontrol edin:

- önemli iç sayfalar;
- giriş/yönetim;
- formlar;
- yüklemeler;
- statik dosyalar;
- veritabanı okuma/yazmaları;
- uygulama/API uç noktaları;
- yönlendirmeler;
- günlükler.

Birçok uygulama gerçek ana makine adı altında ham sunucu IP'sine göre farklı davrandığından hosts dosyası testi özellikle yararlıdır.

Mevcut canlı site söz konusuysa [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberindeki daha sıkı geçiş sürecini kullanın.

## Alan adını VPS'e yönlendirin {#point-the-domain-to-the-vps}

DNS sağlayıcısında bu sunucuya ulaşması gereken kayıtları yapılandırın.

Tipik IPv4 kurulumu:

| Ad | Tür | Değer |
|---|---|---|
| `@` | A | VPS IPv4 adresi |
| `www` | CNAME | kök alan adı |

`www` için A kaydı da kullanılabilir.

AAAA kaydını yalnızca VPS'te IPv6 gerçekten yapılandırılmış ve erişilebilirse ekleyin. Bozuk AAAA kaydı, IPv4 çalışırken bile bazı ziyaretçilerin bağlantısını bozabilir.

DNS tek başına siteyi çalıştırmaz: Nginx/Apache site yapılandırması da eşleşen ana makine adını içermelidir.

Mevcut canlı siteyi taşıyorsanız DNS geçişi ve son yazma işlemleri [web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) rehberinde ele alınır.

## DNS çözümlendikten sonra HTTPS ekleyin {#add-https-after-dns-resolves}

Genel ana makine adı, doğrulama isteğine yanıt verecek sunucuya çözümlendikten sonra güvenilir sertifika alın. Güvenlik duvarı ve sağlayıcı ağ kurallarının kullanacağınız HTTP/HTTPS doğrulama yoluna önceden izin verdiğinden emin olun.

Nginx/Apache için Certbot gibi ACME istemcisi Let's Encrypt sertifikası isteyip yenileyebilir. Eski paket komutunu körlemesine kopyalamak yerine güncel Certbot/işletim sistemi talimatlarını izleyin.

Şunları doğrulayın:

- sertifika kullandığınız kök ve `www` adlarını kapsıyor;
- HTTP amaçlandığı gibi HTTPS'e yönleniyor;
- sertifika yenilemesi otomatik;
- yenileme güvenlik duvarı/CDN yapılandırmasından geçebiliyor;
- uygulama doğru HTTPS URL'leri oluşturuyor.

Sertifika yolunun çalıştığını bilmeden HTTPS yönlendirmesini etkinleştirmeyin.

## Güvenlik duvarını yapılandırın {#configure-the-firewall}

Güvenlik duvarı kurallarını değiştirirken yönetici erişimini çalışır tutun.

Temel bir herkese açık site çoğunlukla şunları gerektirir:

- gerekli yönetim kaynağı/yolu üzerinden SSH;
- HTTP/ACME/yönlendirmeler için TCP 80;
- HTTPS için TCP 443.

Varsayılan olarak yerelde dinliyorlar diye MySQL/PostgreSQL, Redis veya iç uygulama portlarını herkese açmayın.

UFW kullanan sunucuda kısıtlayıcı kuralları etkinleştirmeden **önce** gerekli SSH yoluna izin verin.

Ayrıntılı güvenlik duvarı ve sıkılaştırma bilgileri [VPS güvenlik kontrol listesinde]({{< relref "vps-security-checklist.md" >}}) bulunur.

## Cron görevleri, kuyruklar ve işçi süreçleri {#cron-jobs-queues-and-workers}

Dinamik siteler kurulumdan sonra çoğu zaman yalnızca web isteği yolu yapılandırıldığı için aksar.

Envanter:

- cron görevleri;
- kuyruk işçi süreçleri;
- zamanlanmış işlemler;
- içe/dışa aktarmalar;
- e-posta görevleri;
- önbellek doldurma işleri;
- arka plan işleyicileri.

Bunların şunları yapmasını sağlayın:

- doğru, root olmayan kullanıcıyla çalışmak;
- gerektiğinde otomatik başlamak;
- bilinen günlüklere yazmak;
- CPU/RAM'i tüketen çakışmalardan kaçınmak;
- sunucu yeniden başlatmasından sonra çalışmaya devam etmek.

## Günlükler ve temel gözlemlenebilirlik {#logs-and-basic-observability}

Canlı trafikten önce site arızalandığında nereye bakacağınızı bilin.

En azından şunları belirleyin:

- Nginx/Apache erişim günlüğü;
- Nginx/Apache hata günlüğü;
- uygulama günlüğü;
- PHP-FPM/çalışma ortamı günlüğü;
- veritabanı günlüğü/durumu;
- sistem günlüğü;
- disk kullanımı;
- bellek/CPU baskısı.

VPS'e kimse bağlı değilken de sunucu arızasının görünmesi için harici HTTP(S) erişilebilirlik kontrolü ekleyin.

Ayrıntılı eşik ve uyarı tasarımı [VPS izleme]({{< relref "vps-monitoring.md" >}}) rehberindedir.

## Yeniden başlatma doğrulaması {#reboot-validation}

Şaşırtıcı sayıda ilk VPS kurulumu yalnızca ilk yeniden başlatmaya kadar çalışır.

Sunucuyu hazır saymadan önce:

```bash
sudo reboot
```

Geri geldiğinde şunları doğrulayın:

- SSH erişimi;
- Nginx/Apache;
- PHP-FPM veya uygulama servisi;
- veritabanı;
- cron/kuyruk işçi süreçleri;
- HTTPS;
- site sayfaları/formları;
- izleme;
- yedekleme zamanlaması.

Uygulama yalnızca birisi manuel komut çalıştırınca dönüyorsa kurulum tamamlanmamıştır.

## Manuel / panelsiz hosting ne zaman uygun değildir? {#when-manual--no-panel-hosting-is-the-wrong-fit}

Şu durumlarda kontrol paneli veya yönetim hizmeti kullanın:

- SSH ve komut satırından kurtarma konusunda rahat kimse yoksa;
- işletim sistemi/güvenlik güncellemelerini kimse üstlenmiyorsa;
- web sunucusu/çalışma ortamı/veritabanı arızalarını kimse teşhis edemiyorsa;
- yedekler oluşturuluyor ama kimse geri yükleyemiyorsa;
- iş açısından kritik kesintinin müdahale sorumlusu yoksa;
- ekip e-posta, kullanıcı ve alan adlarını sunucu yapılandırması yerine hosting arayüzünden yönetmek istiyorsa;
- uygulama ortamı yönetilen platformda daha iyi karşılanıyorsa.

Manuel VPS panel yükünü azaltıp kontrolü artırabilir; ancak işletim sorumluluğunun miktarını azaltmaz.

Panel seçimi için [kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}), eksik olan işletim sorumlusuysa [yönetilen ve yönetilmeyen VPS karşılaştırmasını]({{< relref "managed-vs-unmanaged-vps.md" >}}) kullanın.

## Canlı ortam kabul kontrol listesi {#production-acceptance-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| Sunucu erişimi | kişisel yönetici hesabı giriş yapabiliyor; kurtarma konsolu erişilebilir |
| Güncellemeler | güncel güvenlik/sistem güncellemeleri uygulanmış |
| Web sunucusu | otomatik başlıyor ve yapılandırma testi başarılı |
| Site ana makine adı | kök/`www` davranışı bilinçli belirlenmiş |
| DNS | A/AAAA/CNAME istenen sunucuya/yola çözümleniyor |
| HTTPS | güvenilir sertifika, doğru adlar, bilinen yenileme yolu |
| Uygulama | temsili sayfalar, giriş, formlar ve yüklemeler çalışıyor |
| Veritabanı | uygulama kullanıcısı çalışıyor; veritabanı portu yanlışlıkla herkese açık değil |
| Dosyalar | doğru sahiplik; `777` geçici çözümü yok |
| Görevler | cron/işçi süreçleri doğru başlıyor ve günlük yazıyor |
| Yeniden başlatma | gerekli servisler otomatik geri geliyor |
| Günlükler | yönetici web/uygulama/sistem hatalarının nerede göründüğünü biliyor |
| Yedek | gerekli dosyalar/veritabanı dahil; geri yükleme yolu tanımlı |
| İzleme | harici site kontrolü ve temel kaynak görünürlüğü |
| Kapasite | CPU/RAM/disk gerçek yük altında kontrol edilmiş |

Ana sayfa HTTP 200 döndürüyor diye site canlı kullanıma hazır değildir.

## Yedekleme ve izlemeye geçiş {#backups-and-monitoring-handoff}

Bu sayfa yalnızca temel geçiş koşullarını belirler.

Siteye güvenmeden önce:

- yedekleri zamanlayın;
- bağımsız/sunucu dışı kopya tutun;
- veritabanını ve kurtarma için gereken yapılandırma/gizli bilgileri dahil edin;
- geri yüklenebilirliği doğrulayın;
- site erişilebilirliğini izleyin;
- disk büyümesini izleyin;
- CPU/RAM/veritabanı baskısını takip edin;
- sertifika yenilemesini izleyin.

Ayrıntılı kurtarma tasarımı [VPS yedekleme stratejisinde]({{< relref "vps-backup-strategy.md" >}}), izleme eşikleri ve uyarı tasarımı [VPS izleme]({{< relref "vps-monitoring.md" >}}) rehberinde ele alınır.

## Birden fazla web sitesi {#multiple-websites}

Birkaç site için:

- her ana makine adına ayrı sunucu bloğu/sanal konak kullanın;
- site kök dizinlerini ayırın;
- ayrı uygulama/veritabanı erişim bilgileri kullanın;
- güven modeli gerektiriyorsa ayrı sistem kullanıcıları kullanın;
- tek sitenin cron, içe aktarma veya yedeklerinin diğerlerini kaynaksız bırakmasını önleyin;
- toplam yoğun yükü hesaba katın;
- tüm sitelerin hâlâ tek VPS arıza alanını paylaştığını bilin.

Kapasite ve yalıtım planı için [birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) rehberini kullanın.

## Teknik kaynaklar {#technical-references}

- Ubuntu Server: Nginx kurulumu
- Ubuntu Server: Nginx yapılandırması
- Ubuntu Server: web servisleri
- VDSina Standard VPS — güncel sade işletim sistemi şablonları

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Web siteniz için VPS seçin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır. İş ortaklığı bağlantıları sponsored olarak işaretlidir. Siparişten önce güncel VPS fiyatlarını, işletim sistemi seçeneklerini ve sağlayıcı koşullarını doğrulayın.</small></p>

## Sık sorulan sorular {#faq}

### Kontrol paneli olmadan VPS'te site barındırabilir miyim? {#can-i-host-a-website-on-a-vps-without-a-control-panel}

Evet. Temiz Linux VPS; SSH ve uygulamanın ihtiyaç duyduğu web sunucusu, çalışma ortamı ve veritabanı bileşenleriyle site barındırabilir. Panelsiz kurulum bu rehberin bir parçasıdır.

### VPS'te site barındırmak için Nginx gerekir mi? {#do-i-need-nginx-to-host-a-website-on-vps}

Hayır. Nginx ve Apache yaygın seçeneklerdir. Uygulamaya, yapılandırmaya ve yöneticinin deneyimine uyan web sunucusunu kullanın.

### VPS'teki her site veritabanı gerektirir mi? {#does-every-vps-website-need-a-database}

Hayır. Statik siteler gerektirmez. MySQL/MariaDB/PostgreSQL'i yalnızca uygulama veritabanı gerektiriyorsa kurun.

### Siteyi barındırmak için root kullanmalı mıyım? {#should-i-use-root-to-host-the-website}

Hayır. Root yönetim içindir. Siteyi yalnızca gereken izinlere sahip uygun root olmayan kullanıcı ve servislerle çalıştırın/dağıtın.

### Ne zaman kontrol paneli kullanmalıyım? {#when-should-i-use-a-control-panel}

Site, alan adı, PHP, veritabanı, kullanıcı, e-posta veya yedekleri tarayıcıdan yönetmek; ek yükü ve kısıtları haklı çıkaracak kadar tekrarlayan yönetim işini azaltıyorsa kullanın.

### cPanel olmadan VPS'te WordPress barındırabilir miyim? {#can-i-host-wordpress-on-a-vps-without-cpanel}

Evet. WordPress uyumlu web sunucusu, PHP, veritabanı, WordPress dosyaları, doğru izinler, DNS ve HTTPS gerektirir. Panel isteğe bağlıdır.

### DNS'i VPS'e ne zaman yönlendirmeliyim? {#when-should-i-point-dns-to-the-vps}

Yeni site için sunucu gerçek ana makine adına yanıt vermeye hazır olduğunda. Mevcut canlı sitede önce test edin, kontrollü taşıma/geçiş planı kullanın.

### Alan adım VPS'e yönlendiği halde neden yanlış site görünüyor? {#why-does-my-domain-point-to-the-vps-but-show-the-wrong-site}

DNS yalnızca ana makine adını sunucu IP'sine gönderir. Nginx/Apache'de o adla eşleşen sunucu bloğu veya sanal konak da bulunmalıdır.

### HTTPS'i ne zaman etkinleştirmeliyim? {#when-should-i-enable-https}

Genel ana makine adı sunucuya çözümlendikten ve doğrulama yolu çalıştıktan sonra. Ardından sertifikayı alın, kök/`www` kapsamını doğrulayın ve amaçlanan HTTP'den HTTPS'e yönlendirmeyi yapılandırın.

### VPS'i yeniden başlattıktan sonra neyi kontrol etmeliyim? {#what-should-i-check-after-rebooting-the-vps}

Web sunucusunun, uygulama servisi/PHP-FPM'in, veritabanının, işçi süreçlerinin, HTTPS'in, izlemenin ve sitenin manuel müdahale olmadan geri döndüğünü doğrulayın.
