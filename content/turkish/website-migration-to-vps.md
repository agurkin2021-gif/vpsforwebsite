---
title: "Web sitesini VPS sunucuya taşıma"
description: "Web sitesini VPS sunucuya taşıma: envanter çıkarın, yeni sunucuyu test edin, son verileri eşitleyin, DNS'i güvenle değiştirin; e-posta, SEO ve geri dönüş yolunu koruyun."
image: "images/home/vps-for-website-hero.webp"
slug: "web-sitesini-vps-sunucuya-tasima"
---

Web sitesini VPS sunucuya taşımanın en güvenli yolu, eski hosting trafiği sunmaya devam ederken yeni sunucuyu kurup test etmektir. Mevcut yazılımların envanterini çıkarın, hedef kaynakları seçin, siteyi kopyalayıp doğrulayın, son veri değişikliklerini kontrol edin, DNS'i en son değiştirin ve eski hosting kapatılabilene kadar iki ortamı da izleyin.

Bu sayfa alan adının ve herkese açık URL yapısının değişmediğini varsayar. Alan adı veya yollar da değişiyorsa URL eşleme ve kalıcı yönlendirmeler ayrı taşıma işi haline gelir.

Genel hosting kararı için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[Hızlı plan](#quick-migration-plan) · [Ön kontrol aracı](#migration-cutover-preflight) · [Son eşitleme](#control-new-writes-and-the-final-sync) · [DNS geçişi](#switch-dns-deliberately) · [SEO kontrolleri](#preserve-seo-when-urls-stay-the-same) · [Sık sorulan sorular](#faq)

## Hızlı taşıma planı {#quick-migration-plan}

Kontrollü taşıma şu sırayı izler:

1. **Kaynağın envanterini çıkarın.** Uygulamayı, çalışma ortamını, veritabanını, dosyaları, DNS'i, e-postayı, cron görevlerini, işçi süreçlerini, webhook'ları ve harici bağımlılıkları kaydedin.
2. **Hedef kaynakları seçin.** CPU, RAM ve diski gerçek yük ve taşıma payına göre belirleyin.
3. **Geri yüklenebilir yedek oluşturun.** Kaynak sunucunun dışında kopya tutun; gereken veritabanı ve dosyaların gerçekten bulunduğunu doğrulayın.
4. **VPS'i paralel kurun.** Trafik taşınmadan önce web yazılımlarını veya paneli kurup uygulama gereksinimlerini karşılayın.
5. **İlk tam veri kümesini kopyalayın.** Eski site yayında kalırken dosyaları aktarın ve veritabanını içe alın.
6. **Özel olarak test edin.** DNS değişmeden önce yeni sunucuyu hosts dosyası, kontrollü önizleme adı veya eşdeğer yöntemle sınayın.
7. **Son yazmaları kontrol edin.** Mağaza, üyelik, form ve diğer değişen sitelerde kısa yazma duraklatması veya uygulamaya uygun son fark eşitlemesi planlayın.
8. **DNS'i en son değiştirin.** Yalnızca taşınması gereken kayıtları değiştirin; e-posta ve doğrulama kayıtlarını koruyun.
9. **İki sunucuyu da izleyin.** Trafiği, hataları, formları, siparişleri, cron'u, webhook'ları, e-postayı, HTTPS'i ve arama motoru taramasını doğrulayın.
10. **Eski hostingi yalnızca kabulden sonra kapatın.** Geri dönüş süresi boyunca erişilebilir tutun.

Her durum için dürüst bir sıfır kesinti vaadi yoktur. Hedef, uygulanabilir en kısa kesinti ve plansız veri kaybı olmadan kontrollü geçiştir.

## Gerçekte neyin taşındığını belirleyin {#define-what-is-actually-moving}

“Siteyi taşımak” birkaç farklı sistemi kapsayabilir. Kopyalamadan önce kapsamı belirleyin.

| Bileşen | Taşımadan önce yanıtlanacaklar |
|---|---|
| Site / uygulama | CMS veya framework, site kök dizini, yüklemeler, gizli dosyalar, önbellek, yazılabilir dizinler |
| Çalışma ortamı | PHP/Node/Python sürümü, eklentiler/modüller, web sunucusu, süreç yöneticisi |
| Veritabanı | motor/sürüm, boyut, kullanıcılar/izinler, karakter kümesi, zamanlanmış bakım |
| DNS | sağlayıcı, A/AAAA/CNAME kayıtları, www/kök davranışı, TTL, doğrulama kayıtları |
| E-posta | barındırıldığı yer, MX, SPF, DKIM, DMARC, posta kutuları, yönlendirmeler, SMTP |
| Zamanlanmış işler | cron, kuyruklar, işçi süreçleri, içe/dışa aktarmalar, yedekler, zamanlanmış işlemler |
| Harici sistemler | ödeme webhook'ları, API'ler, IP izin listeleri, CDN/WAF, analitik, Search Console |
| Güvenlik / gizli bilgiler | ortam değişkenleri, API anahtarları, SSH anahtarları, TLS, güvenlik duvarı kuralları |

Gerekçe olmadan ilgisiz değişiklikleri birleştirmeyin. Alan adı, URL yapısı, uygulama sürümü ve büyük yazılım yükseltmeleri aynı anda değişmediğinde hosting taşımasında teşhis daha kolaydır.

## Taşıma geçişi ön kontrolü {#migration-cutover-preflight}

DNS değiştirmeden önce bu aracı kullanın. Başarılı taşıma garantisi vermez; önce çözülmesi gereken eksik ön koşulları gösterir.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="migration-preflight">
  <div class="mb-6">
    <label for="mig-backup" class="form-label">Bağımsız yedek var, geri yükleme/içe aktarma test edildi</label>
    <select id="mig-backup" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-sizing" class="form-label">Hedef CPU, RAM ve disk kapasite payıyla seçildi</label>
    <select id="mig-sizing" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-runtime" class="form-label">Çalışma ortamı, veritabanı ve gerekli eklentiler uyumlu</label>
    <select id="mig-runtime" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-test" class="form-label">Yeni site DNS geçişinden önce özel olarak test edildi</label>
    <select id="mig-test" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-dns" class="form-label">DNS kayıtları belgelendi, TTL/geçiş planlandı</label>
    <select id="mig-dns" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-mail" class="form-label">E-posta konumu ve MX/SPF/DKIM/DMARC işlemleri belirlendi</label>
    <select id="mig-mail" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option><option value="na">Uygulanamaz / e-posta ayrı ve değişmiyor</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-writes" class="form-label">Sipariş, form, üye veya yüklemeler için son yazma/veri eşitleme planı var</label>
    <select id="mig-writes" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır / site fiilen salt okunur</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-tls" class="form-label">HTTPS/TLS hedefte gerçek ana makine adıyla çalışabiliyor</label>
    <select id="mig-tls" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-jobs" class="form-label">Cron, işçi süreçleri, webhook'lar ve IP izin listeleri belgelenmiş ve kontrollü</label>
    <select id="mig-jobs" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option><option value="na">Uygulanamaz</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-rollback" class="form-label">Geri dönüş koşulu tanımlı, eski hosting erişilebilir kalacak</label>
    <select id="mig-rollback" class="form-input"><option value="no">Hazır değil</option><option value="yes">Hazır</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Geçiş hazırlığını kontrol edin</button>
</form>
<p id="migration-preflight-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Gerçekten hazır olan maddeleri işaretleyin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("migration-preflight");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var items = [
      ["mig-backup", "bağımsız yedek"],
      ["mig-sizing", "hedef kaynak seçimi"],
      ["mig-runtime", "çalışma ortamı/veritabanı uyumu"],
      ["mig-test", "hedefin özel ortamda test edilmesi"],
      ["mig-dns", "DNS/TTL planı"],
      ["mig-mail", "e-posta/DNS e-posta planı"],
      ["mig-writes", "son yazma/veri eşitleme planı"],
      ["mig-tls", "HTTPS/TLS hazırlığı"],
      ["mig-jobs", "cron/worker/webhook/izin listeleri"],
      ["mig-rollback", "geri dönüş planı"]
    ];

    function isComplete(id) {
      var value = document.getElementById(id).value;
      return value === "yes" || value === "na";
    }

    var missing = items.filter(function (item) {
      return !isComplete(item[0]);
    }).map(function (item) {
      return item[1];
    });

    var result;
    if (missing.length === 0) {
      result = "KONTROLLÜ GEÇİŞE HAZIR: gerekli tüm maddeler hazır veya açıkça uygulanamaz olarak işaretlendi. DNS değişikliğinden hemen önce son veri eşitlemesini ve geri dönüş koşulunu yeniden kontrol edin.";
    } else {
      result = "GEÇİŞE HAZIR DEĞİL: önce şu eksikleri tamamlayın: " + missing.join(", ") + ".";
    }

    document.getElementById("migration-preflight-result").textContent = result;
  });
});
</script>

## Mevcut sitenin envanterini çıkarın {#inventory-the-current-website}

Hedefte işlem yapmadan önce taşıma kaydı oluşturun.

Şunları kaydedin:

- alan adı ve tüm etkin alt alan adları;
- uygulama/CMS/framework sürümü;
- PHP, Node.js, Python veya diğer çalışma ortamı sürümü;
- veritabanı motoru/sürümü, boyutu ve erişim modeli;
- site kök dizini ve dışındaki dizinler;
- yüklemeler/medya ve yazılabilir dizinler;
- yönlendirmeler ve yeniden yazma kuralları;
- cron görevleri, kuyruklar, işçi süreçleri ve zamanlanmış işler;
- kullanılıyorsa Redis gibi önbellek servisleri;
- SSL/TLS yapılandırması;
- DNS kayıtları;
- posta kutuları, yönlendirmeler ve giden SMTP yolu;
- ödeme geçitleri, webhook'lar ve API geri çağrıları;
- üçüncü taraf IP izin listeleri;
- CDN/WAF/kaynak sunucu kısıtları;
- Search Console/analitik doğrulaması;
- mevcut depolama kullanımı ve büyümesi.

Envanter aynı zamanda taşıma sonrası kabul listesidir: her madde VPS'te çalışmalı veya bilinçli olarak harici serviste bırakılmalıdır.

## Hedef VPS kaynaklarını seçip hazırlayın {#size-and-prepare-the-destination-vps}

Önce taşıyıp sonra VPS yeterince büyük mü diye sormayın.

Hedefi seçerken mevcut yükü, veritabanı davranışını, depolama artışını, panel/e-posta yükünü ve taşıma çalışma alanını kullanın. Taşımanın kendisi arşivler, veritabanı dökümleri, günlükler ve yerel yedek hazırlığı için geçici disk gerektirebilir.

Kaynak hesabı için [web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}) rehberini kullanın.

Taşıma aynı zamanda yönetim yolu kararıdır. Eski hosting sunucu yönetiminin çoğunu görünmez kılıyorsa önce geçişten sonra hedefi kimin işleteceğini belirleyin: [yönetilen ve yönetilmeyen VPS karşılaştırmasını]({{< relref "managed-vs-unmanaged-vps.md" >}}) inceleyin. Ardından hedefte panel mi manuel Linux ortamı mı kullanılacağını seçin; bunun için [kontrol panelli VPS]({{< relref "vps-with-control-panel.md" >}}) rehberine bakın.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Hedef VPS'i seçin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır ve bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Taşıma rehberliği ve kaynak seçimi ölçütleri komisyona göre değişmez.</small></p>

## Geri dönüşü mümkün kılan yedek oluşturun {#create-a-rollback-capable-backup}

Yedek yalnızca gereken veriyi içeriyor ve geri yüklenebiliyorsa yararlıdır.

Taşımadan önce:

1. site dosyalarının güncel kopyasını oluşturun;
2. gerekli tüm veritabanlarını dışa aktarın;
3. kaynak hosting hesabı dışında kopya saklayın;
4. yapılandırma dosyalarını ve ortam değişkenlerini güvenle kaydedin;
5. DNS ve e-posta kayıtlarını ayrıca kaydedin;
6. mümkünse yedeği geçici/test ortamına geri yükleyin; en azından yalnızca arşivin açıldığını kontrol etmek yerine gerçek veritabanı içe aktarması yapıp temsili dosyaları doğrulayın;
7. geri yüklenen kopyanın beklenen verileri içerdiğini ve geri dönüşü destekleyecek kadar başlatılabildiğini doğrulayın;
8. DNS değişmeden önce geri dönüş sırasını yazın.

Dinamik sitede ilk yedek son canlı veri kümesi değildir. İlk kopyadan sonra siparişler, form gönderimleri, yorumlar, üyelikler veya yüklemeler değişmeye devam edebilir. Son fark aktarımını ayrıca planlayın.

## DNS değişmeden önce hedefi kurun {#build-the-destination-before-dns-changes}

Hedef, genel trafik gelmeden önce siteyi çalıştırabilmelidir.

Şunları eşleştirin veya bilinçli biçimde doğrulayın:

- web sunucusu davranışı;
- PHP/Node/Python sürümü;
- gerekli eklentiler/modüller;
- veritabanı motoru/sürümü;
- dosya sahipliği ve izinler;
- yükleme/istek gövdesi boyut sınırları;
- zamanlanmış görev ortamı;
- önbellek servisleri;
- yeniden yazma/yönlendirme kuralları;
- ortam değişkenleri ve gizli bilgiler;
- SMTP/giden ağ ihtiyaçları;
- güvenlik duvarı kuralları;
- uygulamaya özgü yollar.

Zorunlu değilse taşımayı bütün çalışma ortamlarını yükseltme veya yazılımları yeniden kurma anına dönüştürmeyin. Daha az eşzamanlı değişiklik, geri dönüşü ve teşhisi kolaylaştırır.

## Dosyaları ve veritabanını kopyalayın {#copy-files-and-database}

Tam aktarım yöntemi kaynak erişimine bağlıdır.

Tipik kaynak yolları:

- cPanel/Dosya Yöneticisi + phpMyAdmin dışa aktarmaları;
- kabuk erişimi yoksa SFTP/FTP;
- iki taraf da izin veriyorsa SSH/rsync;
- CMS'e özgü taşımalar için uygulamayı tanıyan taşıma araçları;
- sağlayıcının dışa aktarma/yedek araçları.

Uygulama gerektiriyorsa yeniden yazma kuralları gibi gizli yapılandırma dosyalarını koruyun. İçe aktardıktan sonra veritabanı kullanıcısını, yetkileri, karakter kümesi/sıralama varsayımlarını ve uygulama bağlantı ayarlarını doğrulayın.

Büyük veri kümelerinde “aktarım tamamlandı” ifadesini “veriler aynı” saymak yerine mümkünse boyutları, satır sayılarını veya sağlama toplamlarını karşılaştırın.

## Geçişten önce özel olarak test edin {#test-privately-before-cutover}

DNS'i test edilmemiş sunucuya yönlendirmeyin.

Hedefi hosts dosyası, kontrollü önizleme adı veya gerçek uygulama ortamını sınayan başka özel yöntemle test edin.

Şunları kontrol edin:

- ana sayfa ve temsili iç sayfalar;
- yönetici girişi;
- kullanıcı girişi;
- görseller, CSS, JavaScript ve indirmeler;
- arama;
- formlar ve gönderim teslimatı;
- yüklemeler;
- yönlendirmeler;
- API uç noktaları;
- ödeme ve ödeme geri çağrıları;
- cron/zamanlanmış işlemler;
- kuyruklar/işçi süreçleri;
- giden e-posta;
- uygulama, web sunucusu ve veritabanı günlükleri;
- mobil düzen ve gezinme.

Geçici genel ana makine adı aramada yanlışlıkla kopya sayfaya dönüşmemelidir. Test sırasında herkese açıksa dizin dışında tutun; geçişten önce gerçek canlı ana makine adındaki geçici engellemeyi kaldırın.

## Yeni yazmaları ve son eşitlemeyi kontrol edin {#control-new-writes-and-the-final-sync}

Tanıtım sitesi ile işlem yapan site arasındaki en önemli fark budur.

DNS geçişinde eski ve yeni veritabanı yazma kabul ederse verileri ayrışabilir. Eski sunucuya kaydedilen sipariş kendiliğinden yenisinde görünmez.

Değişen sitelerde:

1. düşük riskli geçiş aralığı seçin;
2. mümkünse kaynakta yeni yazmaları duraklatın veya kontrol edin;
3. veriyi iki kez yazabilecek cron ve kuyruk süreçlerini durdurun veya kontrol edin;
4. son veritabanı eşitlemesini yapıp değişen yükleme/dosyaları kopyalayın;
5. son yetkili veri kaynağının zamanını kaydedin;
6. trafiği değiştirin;
7. yeni yazmaların artık yalnızca hedefe gittiğini doğrulayın.

[WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) taşırken kabul testine ödeme, siparişler, ödeme webhook'ları, stok, zamanlanmış işlemler ve işlem e-postalarını dahil edin. Statik/önbellekli site yalnızca son dosya karşılaştırmasını gerektirebilir.

Uygulama ve eşitleme yöntemi gerçekten desteklemiyorsa taşımayı “sıfır kesinti” olarak adlandırmayın.

## DNS'i bilinçli değiştirin {#switch-dns-deliberately}

DNS trafik anahtarıdır; ilk taşıma adımı değildir.

Geçişten önce:

- mevcut DNS bölgesini dışa aktarın veya kaydedin;
- değişecek A/AAAA/CNAME/kaynak sunucu kayıtlarını tam belirleyin;
- mümkünse ilgili TTL'yi planlanan geçişten en az bir eski TTL süresi önce düşürün; örneğin mevcut TTL 86,400 saniyeyse değişiklikten 24 saatten daha önce azaltın;
- TTL'yi şimdi düşürmenin eski uzun TTL'yi kaydetmiş önbellekleri silmediğini unutmayın;
- taşınmayan MX, SPF, DKIM, DMARC, doğrulama TXT, SRV, CAA ve diğer kayıtları koruyun;
- hem kök hem www davranışını doğrulayın.

DNS sağlayıcısı değişmiyorsa A/AAAA kaydını değiştirmek çoğunlukla ad sunucularını değiştirmekten az risklidir. Ad sunucuları değişecekse gereken bölgenin tamamını önce yeniden oluşturun.

Geçişten sonra genel DNS'i birden fazla çözümleyici/ağdan doğrulayın; trafiğin eski sunucudan yenisine geçişini izleyin.

## E-postanın bozulmasını önleyin {#keep-email-from-breaking}

Eski paylaşımlı hesap birlikte sunsa bile site taşıma ve e-posta taşıma ayrı işlerdir.

Geçişten önce bir yol seçin:

- e-postayı mevcut/yönetilen sağlayıcıda tutup MX/TXT kayıtlarını korumak;
- e-postayı başka yönetilen sağlayıcıya taşımak;
- e-postayı VPS'e taşıyıp kutuları, yönlendirmeyi, kimlik doğrulamayı ve teslimat kontrollerini yeniden kurmak.

E-posta taşınıyorsa şunları hesaba katın:

- MX öncelikleri;
- SPF;
- DKIM;
- DMARC;
- uygulanıyorsa ters DNS/PTR;
- posta kutusu verileri;
- takma adlar/yönlendirmeler;
- SMTP erişim bilgileri;
- spam filtreleme;
- yedekler ve gönderici itibarı.

E-posta kayıtları ve diğer bağımlılıklar yeniden oluşturulmadıkça yalnızca siteyi taşımak için tüm DNS bölgesini değiştirmeyin.

## HTTPS, CDN ve harici servisleri doğrulayın {#verify-https-cdn-and-external-services}

Hedef bölge hâlâ seçilmediyse geçişten önce [VPS sunucu konumu seçimi]({{< relref "how-to-choose-vps-location.md" >}}) rehberiyle belirleyin. Bölgeyi sonra değiştirmek yeni bir IP/DNS taşıması gerektirebilir.

IP üzerinden çalışan hedef, gerçek ana makine adı altında yine de başarısız olabilir.

Şunları doğrulayın:

- TLS sertifikası gerekli ana makine adlarını kapsıyor;
- HTTP → HTTPS yönlendirmesi doğru;
- kök ↔ www kanonik davranışı değişmemiş;
- HSTS varsayımları biliniyor;
- CDN/WAF yeni kaynak sunucuya yönleniyor veya izin veriyor;
- proxy kullanılıyorsa gerçek istemci IP'si işleme hâlâ çalışıyor;
- ödeme webhook'ları yeni kaynak sunucuya ulaşıyor;
- eski sunucu IP'sini izin listesine alan API sağlayıcıları güncellenmiş;
- SMTP/API erişim bilgileri yeni sunucudan geçerli.

Geçici güvenlik duvarı/WAF istisnalarını dar tutup kabulden sonra kaldırın.

## URL'ler aynı kaldığında SEO'yu koruyun {#preserve-seo-when-urls-stay-the-same}

Yalnızca hosting değişikliği normalde herkese açık URL'leri aynı tutar. Bu durumda SEO işi çoğunlukla yönlendirme eşlemek değil, **eşdeğerliği korumaktır**.

Geçişten önce ve sonra şunları karşılaştırın:

- HTTP durum kodları;
- kanonik URL'ler;
- robots.txt;
- meta robots / yanlışlıkla noindex;
- site haritası URL'leri;
- iç bağlantılar;
- önemli yerlerde yapılandırılmış veriler;
- sayfa içeriği ve işlenen dosyalar;
- Search Console doğrulaması;
- Googlebot ve normal kullanıcılara sunucu yanıtları.

Google Search Central; yeni hostingi hazırlayıp test etmeyi, DNS'i yalnızca hazırken değiştirmeyi, eski ve yeni ortamı izlemeyi, trafik taşındıktan sonra eski altyapıyı kapatmayı önerir. DNS TTL'sini önceden düşürmeyi ve Search Console doğrulamasını çalışır tutmayı da önerir.

Yalnızca hosting altyapısı değişiyor, alan adı ve URL'ler aynı kalıyorsa **Google Search Console'un Adres Değişikliği aracını kullanmayın**. Araç, aynı URL'li hosting taşıması için değil alan adı değişikliği içindir.

Alan adı veya URL yolları da değişiyorsa eski-yeni URL eşlemesi ve kalıcı sunucu tarafı yönlendirmeler kullanın. Bu, aynı URL'li VPS taşımasından farklı site taşıma problemidir.

## Geçiş kontrol listesi {#cutover-checklist}

DNS değişiminden hemen önce:

| Kontrol | Başarı koşulu |
|---|---|
| Yedek | bağımsız kopya var; geri yükleme/içe aktarma test edilmiş, temsili veriler doğrulanmış |
| Hedef | doğru çalışma ortamı, veritabanı, izinler ve gizli bilgiler |
| Özel test | sayfalar, formlar, giriş ve gerekiyorsa ödeme/API başarılı |
| Son veriler | son veritabanı/yükleme farkı tamamlanmış; yetkili veri kaynağı zamanı kayıtlı |
| Görevler | eski cron/süreçler kontrollü; yeni görevler planlanan anda başlıyor |
| DNS | değişecek kayıtlar tam belirlenmiş; e-posta/doğrulama kayıtları korunmuş |
| HTTPS | hedef gerçek ana makine adını güvenle sunabiliyor |
| Harici servisler | webhook'lar, izin listeleri, CDN/WAF ve SMTP hesaba katılmış |
| SEO eşdeğerliği | kanonik/robots/site haritası/durum davranışı amaca uygun |
| Geri dönüş | koşul, sorumlu eylem ve eski hosting erişilebilirliği tanımlı |

“Dosyalar kopyalandı” diye geçmeyin. Hedef kabul ölçütlerini geçtiği için geçin.

## Taşıma sonrası kabul ve geri dönüş {#post-migration-acceptance-and-rollback}

DNS değiştikten sonra:

- eski ve yeni sunucunun erişim/hata günlüklerini izleyin;
- yeni kullanıcı etkinliğinin hedef veritabanına ulaştığını doğrulayın;
- formları, ödemeyi, girişleri ve yüklemeleri yeniden test edin;
- cron, kuyruk ve zamanlanmış işlemleri doğrulayın;
- giden e-postayı ve gerekiyorsa gelen e-posta yönlendirmesini doğrulayın;
- CPU, RAM, disk ve veritabanı davranışını izleyin;
- HTTPS ve CDN/WAF davranışını doğrulayın;
- önemli URL'lerde 200/yönlendirme eşdeğerliğini kontrol edin;
- Search Console tarama/dizin göstergelerini izleyin;
- kararlaştırılan kararlılık süresi boyunca eski ortamı erişilebilir tutun.

### Geri dönüşün veri açısından sınırı vardır {#rollback-has-a-data-boundary}

Erken geri dönüş, **yalnızca eski sunucu hâlâ geçerli yetkili veri kaynağıyken** DNS'i geri yönlendirmek kadar basit olabilir.

Sipariş, kayıt, yorum veya yüklemeler yeni sunucuya yazıldıktan sonra yalnızca DNS'i geri almak yeni değişiklikleri kaybettirebilir. O noktada geri dönüş veri uzlaştırması veya planlanmış başka eşitleme gerektirir.

Taşımadan önce geri dönüş koşullarını belirleyin; örneğin:

- yaygın 5xx hataları;
- ödeme işlemi hatası;
- veritabanı bozulması veya eksik yazmalar;
- ağır çalışma ortamı uyumsuzluğu;
- bozuk kimlik doğrulama;
- kararlaştırılan sürede düzeltilemeyen kritik e-posta/webhook hatası.

## WordPress, WooCommerce ve özel uygulama notları {#wordpress-woocommerce-and-custom-application-notes}

### WordPress {#wordpress}

PHP sürümü/eklentilerini, veritabanı uyumunu, yüklemeleri, yeniden yazma kurallarını, wp-cron davranışını, önbelleği, SMTP/iletişim formlarını ve yönetici girişini kontrol edin. Serileştirilmiş veriyi bozabilecek kör arama/değiştirme işlemlerinden kaçının; gerektiğinde uygulamayı tanıyan araçlar kullanın.

Kaynak davranışı için [WordPress için VPS]({{< relref "vps-for-wordpress.md" >}}) rehberine bakın.

### WooCommerce ve diğer işlem odaklı siteler {#woocommerce-and-other-transactional-sites}

Siparişleri, stoku, ödeme geri çağrılarını, oturumları, zamanlanmış işlemleri ve işlem e-postalarını canlı veri olarak ele alın. İlk kopyaya güvenmek yerine son veritabanı/yazma geçişini planlayın.

[WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) rehberine bakın.

### Özel uygulamalar {#custom-applications}

Ortam değişkenlerini, gizli bilgileri, arka plan süreçlerini, kuyrukları, derleme/çalışma ortamı sürümlerini, nesne depolamasını, dosya yollarını, webhook'ları, API izin listelerini ve dağıtım/başlangıç davranışını belgeleyin. Yalnızca IP yanıtını değil, gerçek ana makine adı davranışını test edin.

## Teknik kaynaklar {#technical-references}

- Google Search Central: web hosting değişikliği ve SEO
- Google Search Central: URL değişiklikleriyle site taşıma

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Taşıma için VPS seçin</a>
</p>
<p><small>Açıklama: editörün VDSina ile profesyonel bir ilişkisi vardır. İş ortaklığı bağlantıları sponsored olarak işaretlidir. VPS fiyatları, aktarım kotaları ve diğer sağlayıcı koşulları değişebilir; siparişten önce güncel teklifi doğrulayın.</small></p>

## Sık sorulan sorular {#faq}

### Alan adını değiştirmeden siteyi VPS'e taşıyabilir miyim? {#can-i-migrate-a-website-to-a-vps-without-changing-the-domain}

Evet. Hosting taşıması aynı alan adını ve genel URL'leri koruyabilir. Önce hedefi kurup test edin, ardından trafiği yeni sunucuya göndermek için DNS kayıtlarını değiştirin.

### Siteyi VPS'e taşırken 301 yönlendirmeleri gerekir mi? {#do-i-need-301-redirects-when-moving-a-website-to-a-vps}

Genel URL'ler aynı kalıyorsa gerekmez. Yeni alan adı, protokol/yol değişimi veya yeniden düzenlenen içerik gibi gerçek URL değişikliklerinde yönlendirme gerekir.

### VPS taşımasında kesintiyi nasıl azaltırım? {#how-do-i-reduce-downtime-during-a-vps-migration}

Hedefi paralel hazırlayın, ilgili DNS TTL'sini önceden düşürün, özel test yapın, son yazmaları kontrol edin, son veri eşitlemesini çalıştırın, DNS'i yalnızca kabulden sonra değiştirin ve yayılım sırasında eski hostingi açık tutun.

### E-postayı da VPS'e taşımalı mıyım? {#should-i-move-email-to-the-vps-too}

Otomatik olarak değil. E-postayı yönetilen hizmette tutmak taşıma ve teslimat riskini azaltabilir. Taşınacaksa MX, SPF, DKIM, DMARC, posta kutusu verisi, gerekiyorsa ters DNS ve yedekleri ayrıca planlayın.

### DNS değiştirmeden önce neyi test etmeliyim? {#what-should-i-test-before-changing-dns}

Temsili sayfaları, girişi, formları, yüklemeleri, aramayı, gerekiyorsa ödeme geri çağrılarını, zamanlanmış işleri, API/webhook'ları, giden e-postayı, HTTPS'i, yönlendirmeleri ve uygulama/sunucu günlüklerini test edin.

### Taşımadan sonra eski hostingi ne kadar tutmalıyım? {#how-long-should-i-keep-the-old-hosting-after-migration}

DNS trafiği taşınana, yeni sunucu kararlı hale gelene, yeni yazmalar doğrulanana ve kararlaştırılan geri dönüş süresi dolana kadar tutun. Evrensel sabit saat veya gün yerine günlükleri kullanın.

### WooCommerce'i sipariş kaybetmeden taşıyabilir miyim? {#can-i-migrate-woocommerce-without-losing-orders}

Evet; ancak tek eski veritabanı kopyasına güvenerek değil. Sipariş ve stok değişikliklerinin yazılabilir iki veritabanına bölünmemesi için geçişte yazmaları kontrol edip uygulamaya uygun son eşitlemeyi yapın.

### Hosting taşımak SEO'ya zarar verir mi? {#does-moving-hosting-hurt-seo}

Aynı URL'li hosting değişikliği; hedef aynı içeriği, durum kodlarını, kanonik adresleri ve taranabilirliği sunduğunda sitenin arama sinyallerini korumalıdır. Taşıma sonrası Search Console ve sunucu günlüklerini izleyin; altyapı değişiminde geçici tarama hızı değişiklikleri olabilir.
