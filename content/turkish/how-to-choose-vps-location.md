---
title: "VPS sunucu konumu seçimi"
description: "VPS sunucu konumunu hedef kitle, gerçek ağ rotası, dinamik trafik, bağımlılıklar, CDN ve veri konumu gereksinimlerine göre seçin. Testler ve karar aracıyla karşılaştırın."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-sunucu-konumu-secimi"
---

En iyi VPS konumu, kendiliğinden size en yakın ülke değildir. Bölgeyi **sunucuyla gerçekten gecikmeye duyarlı trafik alışverişi yapan kullanıcı ve sistemlere** göre seçin; satın almadan önce gerçek ağ yolunu doğrulayın.

Çoğu sitede en büyük veya en değerli kitleye yakın başlayın. Sonra ağ yönlendirmesini, dinamik trafiği, veritabanı/API bağımlılıklarını, CDN davranışını ve gerçek veri konumu gereksinimlerini kontrol edin.

Genel VPS kararı için [web sitesi için VPS]({{< relref "_index.md" >}}) rehberine bakın.

[Kısa yanıt](#quick-answer) · [Konum aracı](#vps-location-decision-checker) · [Hedef kitle](#start-with-the-audience) · [Rota testi](#test-the-route-not-just-the-map) · [CDN](#cdn-vs-origin-location) · [Bağımlılıklar](#keep-chatty-dependencies-close) · [Küresel kitle](#global-audience-one-origin--cdn-or-multi-region) · [SEO](#does-vps-location-affect-seo) · [Kontrol listesi](#vps-location-pre-purchase-checklist) · [Sık sorulan sorular](#faq)

## Kısa yanıt {#quick-answer}

Şu sırayı kullanın:

1. **Önemli kullanıcıları bulun.** Ödeme yapan müşterilerin, oturum açmış kullanıcıların ve yoğun saat trafiğinin gerçekten nereden geldiğini belirleyin.
2. **Önemli bağımlılığı belirleyin.** Veritabanı, özel API veya üst servis tarayıcı kadar önemli olabilir.
3. **Yakın bölgeleri kısa listeye alın.** Coğrafya son yanıtı değil, adayları verir.
4. **Gerçek rotaları test edin.** Temsili ağlardan gecikmeyi, rota kararlılığını ve paket kaybını karşılaştırın.
5. **CDN trafiğini kaynak sunucu trafiğinden ayırın.** Önbellekli dosyalar uç noktalara taşınabilir; dinamik istekler kaynak sunucuya ulaşır.
6. **Veri konumu kısıtlarını uygulayın.** Yasal, sözleşmesel veya kurumsal gereksinimler en düşük gecikmeli seçeneğin önüne geçebilir.
7. **Kaynakları ayrı seçin.** Konum, CPU/RAM/depolama hesabının yerini tutmaz.

| Soru | Neyi değiştirir? |
|---|---|
| Önemli kullanıcılar nerede? | ilk bölge adayları |
| Site ne kadar dinamik? | kullanıcıların kaynak sunucu gecikmesini ne kadar hissettiği |
| Veritabanı/API nerede? | bölgeler arası gidiş dönüşlerin baskın olup olmadığı |
| Önde CDN var mı? | statik/önbelleklenebilir trafiğin ne kadarının uç noktalara taşındığı |
| Veri konumu kısıtlı mı? | hangi bölgelerin uygun sayıldığı |
| Aday rotalar gerçekte nasıl performans veriyor? | son bölge seçimi |
| Trafik gerçekten küresel ve dinamik mi? | tek kaynak sunucunun yeterli olup olmadığı |

Evrensel “en iyi VPS ülkesi” yoktur. En iyi konum iş yüküne özgüdür.

## VPS konum karar aracı {#vps-location-decision-checker}

Sağlayıcıları karşılaştırmadan önce doğru **karar yaklaşımını** belirlemek için kullanın. Garantili gecikme tahmini yapmaz veya belirli sağlayıcı konumunu seçmez.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-location-checker">
  <div class="mb-6">
    <label for="loc-audience" class="form-label">Önemli hedef kitle nerede?</label>
    <select id="loc-audience" class="form-input">
      <option value="concentrated">Çoğunlukla tek ülke / yakın bölge</option>
      <option value="split">İki ana bölgeye dağılmış</option>
      <option value="global">Genel olarak küresel / baskın bölge yok</option>
    </select>
  </div>

  <div class="mb-6">
    <label for="loc-dynamic" class="form-label">Kaynak sunucuya ne kadar gecikmeye duyarlı dinamik trafik ulaşıyor?</label>
    <select id="loc-dynamic" class="form-input">
      <option value="low">Düşük — çoğunlukla statik/önbelleklenebilir içerik</option>
      <option value="medium">Orta — CMS/giriş/formlar/bazı önbelleksiz istekler</option>
      <option value="high">Yüksek — ödeme/API/panel/gerçek zamanlı veya yoğun dinamik uygulama</option>
    </select>
  </div>

  <div class="mb-6">
    <label for="loc-dependency" class="form-label">Kritik veritabanı/API/özel bağımlılık nerede?</label>
    <select id="loc-dependency" class="form-input">
      <option value="same">Aynı VPS'te / aynı bölgede çalışacak</option>
      <option value="fixed">Belirli bir harici bölgede sabit</option>
      <option value="distributed">Bağımlılıklar dağınık / tek bölge yok</option>
      <option value="none">Önemli gecikmeye duyarlı bağımlılık yok</option>
    </select>
  </div>

  <div class="mb-6">
    <label for="loc-cdn" class="form-label">CDN, herkese açık statik/önbelleklenebilir içeriği önbellekleyecek mi?</label>
    <select id="loc-cdn" class="form-input">
      <option value="yes">Evet</option>
      <option value="no">Hayır / karar verilmedi</option>
    </select>
  </div>

  <div class="mb-6">
    <label for="loc-compliance" class="form-label">Fiziksel/veri konumu yasa, sözleşme veya iç politikayla sınırlı mı?</label>
    <select id="loc-compliance" class="form-input">
      <option value="no">Bilinen zorunlu kısıt yok</option>
      <option value="yes">Evet / olabilir — yalnızca belirli bölgeler uygun</option>
    </select>
  </div>

  <div class="mb-6">
    <label for="loc-tested" class="form-label">Aday bölgeler temsili kullanıcı ağlarından test edildi mi?</label>
    <select id="loc-tested" class="form-input">
      <option value="no">Hayır</option>
      <option value="yes">Evet</option>
    </select>
  </div>

  <button class="btn btn-primary" type="submit">Konum stratejisini seçin</button>
</form>
<p id="vps-location-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Gerçek hedef kitle ve rota verilerini kullanın; yalnızca haritadan bölge seçmeyin.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-location-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var audience = document.getElementById("loc-audience").value;
    var dynamic = document.getElementById("loc-dynamic").value;
    var dependency = document.getElementById("loc-dependency").value;
    var cdn = document.getElementById("loc-cdn").value;
    var compliance = document.getElementById("loc-compliance").value;
    var tested = document.getElementById("loc-tested").value;

    var result;

    if (compliance === "yes") {
      result = "VERİ KONUMU KISITI: önce adayları gerçek yasal, sözleşmesel veya kurum politikası gereksinimini karşılayan bölgelerle sınırlayın. Sonra uygun bölgelerde ağ rotası ve gecikmeyi karşılaştırın. Bu aracı hukuki danışmanlık olarak kullanmayın.";
    } else if (dependency === "fixed" && dynamic !== "low") {
      result = "ÖNCE BAĞIMLILIK / AYNI BÖLGEDE KONUMLANDIRMA: başka bölgede sabit, sık iletişim kurulan veritabanı veya API yanıt süresine baskın gelebilir. Kullanıcı tarafı ölçümler başka mimarinin daha iyi olduğunu göstermedikçe uygulamayı bu bağımlılığa yakın tutan VPS bölgesini tercih edin.";
    } else if (audience === "global" && dynamic === "high") {
      result = "ÇOK BÖLGE GEREKÇELİ OLABİLİR: gerçekten küresel, gecikmeye duyarlı dinamik yük tek kaynak sunucuyu aşabilir. Bölge eklemeden önce durum çoğaltmayı, veritabanı tutarlılığını, yük devrini ve işletim karmaşıklığını doğrulayın.";
    } else if ((audience === "global" || audience === "split") && cdn === "yes" && dynamic !== "high") {
      result = "MERKEZİ KAYNAK SUNUCU + CDN: kaynak sunucuyu en önemli dinamik trafik ve bağımlılıklara en uygun yerde tutun; CDN önbelleklenebilir içeriği dağınık kullanıcılara yakın sunsun. Kalan dinamik yolu gerçek testlerle doğrulayın.";
    } else if (tested === "no") {
      result = "SATIN ALMADAN ÖNCE TEST EDİN: coğrafya kazananı değil, aday listesini verir. Karar vermeden önce test IP'leri/uç noktaları alın veya kısa ömürlü sunucular kullanıp temsili kullanıcı ağlarından gerçek rotaları karşılaştırın.";
    } else {
      result = "ÖNCE KULLANICI BÖLGESİ: kritik bağımlılıkları ve işletim kısıtlarını kabul edilebilir tutarken, en büyük veya en değerli gecikmeye duyarlı kitle için en iyi performansı veren test edilmiş bölgeyi seçin.";
    }

    document.getElementById("vps-location-result").textContent = result;
  });
});
</script>

## Hedef kitleyle başlayın {#start-with-the-audience}

İlk soru “ben neredeyim?” değildir:

**Bu sunucuyu beklemek zorunda olan kişiler nerede?**

Herkese açık sitede bu çoğunlukla ziyaretçiler ve müşterilerdir. İç uygulamada çalışanlar olabilir. API'de insanın tarayıcısı yerine başka sistem olabilir.

Mantıklı ilk aday, gecikmeye duyarlı trafiğin en yoğun olduğu yere yakın bölgedir.

Otomatik olarak şunların yakınına yerleştirmeyin:

- site sahibi;
- geliştirici;
- fatura adresi;
- alan adı kayıt şirketi;
- şirket merkezi.

Bu yerler yalnızca önemli trafiği de temsil ediyorsa önemlidir.

## Trafiği ticari önemine göre ağırlıklandırın {#weight-traffic-by-business-importance}

Ham ziyaretçi sayısı yanıltıcı olabilir.

Şöyle varsayalım:

- ziyaretlerin %60'ı bir kıtadan anonim blog trafiği;
- %30'u başka bölgeden hesap sayfalarını kullanan ödeme yapan müşteriler;
- %10'u kurum içi çalışanlar.

Blog kapsamlı önbellekleniyor ama müşteriler sürekli dinamik hesap, ödeme veya API uç noktalarına gidiyorsa daha küçük müşteri bölgesi kaynak sunucu yerleşiminde daha önemli olabilir.

Yararlı hedef kitle ağırlıkları:

- gelir sağlayan kullanıcılar;
- oturum açmış kullanıcı oturumları;
- ödeme/hesap trafiği;
- destek/yönetici kullanıcıları;
- yoğun saatte eşzamanlılık;
- API istek hacmi;
- iş açısından kritik ülke veya şehirler.

Yalnızca toplam sayfa görüntülemelerini değil, **kaynak sunucu gecikmesine duyarlı** trafiğin nereden geldiğini belirlemek için analitik ve sunucu günlüklerini kullanın.

## İstekler dinamikleştikçe konum daha önemli olur {#location-matters-more-as-requests-become-more-dynamic}

Statik sayfa çoğunlukla kullanıcıya yakın önbelleklenebilir. Dinamik istek genellikle kaynak sunucuya ulaşmalı, uygulama mantığını çalıştırmalı, veritabanını sorgulayıp dönmelidir.

Bu, konumu şu işler için daha önemli kılar:

- WooCommerce sepeti ve ödeme;
- hesap/giriş sayfaları;
- yönetim panelleri;
- API'ler;
- gösterge panelleri;
- arama/filtre uç noktaları;
- önbelleksiz WordPress istekleri;
- hızlı yanıt gerektiren webhook'lar;
- sunucuyla çok sayıda ardışık gidiş dönüş yapan uygulamalar.

Mağazada uygulama tarafı yük için [WooCommerce için VPS]({{< relref "vps-for-woocommerce.md" >}}) rehberine bakın. Konum ödeme performansının yalnızca bir parçasıdır.

## Coğrafya kazananı değil, kısa listeyi verir {#geography-gives-a-shortlist-not-the-winner}

Fiziksel mesafe gecikmeye alt sınır koyar; ancak internet trafiği haritadaki iki nokta arasında düz çizgi izlemiyor.

Gerçek yol şunlara bağlıdır:

- internet servis sağlayıcısı yönlendirmesi;
- eşler arası bağlantı anlaşmaları;
- transit sağlayıcıları;
- yoğunluk;
- kablo güzergâhları;
- ağ arızaları;
- rota değişiklikleri;
- VPS sağlayıcısının hedef ağa nasıl bağlandığı.

Coğrafi olarak daha yakın veri merkezi, belirli servis sağlayıcısına biraz uzak bölgeden daha kötü ağ yolu sunabilir.

Bu nedenle:

**haritada en yakın ≠ gerçek gecikmesi kendiliğinden en düşük**

Açıkça uzak seçenekleri elemek için coğrafyayı, makul seçenekler arasında seçim için ölçümleri kullanın.

## Yalnızca haritayı değil, rotayı test edin {#test-the-route-not-just-the-map}

Sağlayıcıdan her aday bölge için test IP'si, test dosyası, looking glass veya başka güncel uç nokta isteyin. Yoksa ve maliyet taahhüdü düşükse kısa ömürlü sunucu tahminden daha güvenilir test olabilir.

Gerçek kitleye benzeyen ağlardan test edin.

Tüketici sitesinde yararlı test kaynakları şunlar olabilir:

- hedef pazardaki ev interneti;
- mobil ağlar;
- ilgiliyse ofis/kurum ağları;
- hedef kitle yakınındaki uzak izleme noktaları;
- önemli pazarda birden fazla internet servis sağlayıcısı.

Yönetici başka kıtadaysa yalnızca onun dizüstü bilgisayarından test etmeyin.

### Tek ping değil, tekrarlanan gecikmeleri karşılaştırın {#compare-repeated-latency-not-one-ping}

Tek ping zayıf bulgudur.

Tekrarlanan örnekler kullanın:

```bash
ping -c 30 TEST_IP
```

Windows üzerinde:

```text
ping -n 30 TEST_IP
```

Adayları günün benzer saatlerinde karşılaştırın.

Şunlara bakın:

- tipik gidiş dönüş süresi (RTT);
- tutarlılık;
- büyük sıçramalar;
- uç noktada paket kaybı;
- performansın yoğun saatlerde değişip değişmediği.

VPS'i “iyi” yapan evrensel RTT rakamı yoktur. Yararlı karşılaştırma, gerçek yük için aday bölgeler arasındadır.

### Yolu MTR veya traceroute ile inceleyin {#inspect-the-path-with-mtr-or-traceroute}

Linux'ta tipik MTR raporu:

```bash
mtr -rwzc 50 TEST_IP
```

Traceroute:

```bash
traceroute TEST_IP
```

Windows:

```text
tracert TEST_IP
```

MTR/traceroute şunları gösterebilir:

- beklenmeyen coğrafi dolanmalar;
- kararsız transit;
- büyük gecikme sıçramaları;
- rota değişiklikleri;
- yolun nerede verimsizleştiği.

Ara düğümde görülen paket kaybını otomatik olarak uçtan uca kayıp saymayın. Yönlendiriciler gerçek trafiği normal iletirken teşhis trafiğini sınırlayabilir. Hedef ve tekrarlanan uçtan uca davranış daha önemlidir.

### Yalnızca ICMP değil, HTTP test edin {#test-http-not-only-icmp}

Ping ağın gidiş dönüş davranışını ölçer. Kullanıcı HTTP'yi deneyimler.

Temsili test uç noktası varsa bağlantı ve yanıt sürelerini karşılaştırın:

```bash
curl -o /dev/null -s -w 'connect=%{time_connect} ttfb=%{time_starttransfer} total=%{time_total}\n' https://candidate.example/
```

Canlı uygulamada TTFB kaynak sunucu işini de içerir. Bu kurulumdan sonra yararlıdır; ancak yavaş TTFB'nin yalnızca mesafeye bağlanamayacağı anlamına gelir.

Yayına çıktıktan sonra harici gecikmeyi ve uygulama sağlığını takip etmek için [VPS izleme]({{< relref "vps-monitoring.md" >}}) rehberini kullanın.

## Önemli ağları test edin {#test-the-networks-that-matter}

Bir servis sağlayıcısından çok iyi olan rota, diğerinden vasat olabilir.

Önemli pazarda şunları test edin:

- en az bir büyük tüketici internet sağlayıcısı;
- kullanıcıların büyük bölümü mobilse mobil ağ;
- B2B uygulamalarda kurumsal ağ ve VPN yolları;
- sunucular arası gecikme önemliyse gerçek üst API veya bağımlılık.

Amaç her testte birinci gelen bölgeyi bulmak değildir. Önemli trafik için en uygun dengeyi sağlayan bölgeyi bulmaktır.

## Sık iletişim kuran bağımlılıkları birbirine yakın tutun {#keep-chatty-dependencies-close}

Kullanıcı ile VPS arasındaki yol, bağlantı zincirinin yalnızca bir parçasıdır.

Dinamik bir istek şu yolu izleyebilir:

**tarayıcı → VPS → veritabanı → özel API → VPS → tarayıcı**

VPS kullanıcılara yakın, veritabanı ise uzaktaysa uygulama, tarayıcı bağlantısından çok veritabanını bekleyerek zaman kaybedebilir.

Birbirine sıkı bağlı bileşenleri mümkünse aynı bölgede veya düşük gecikmeli bir ağda tutun:

- web/uygulama sunucusu ve birincil veritabanı;
- PHP/uygulama işçi süreçleri ve Redis;
- uygulama ve özel API;
- istekler eşzamanlı ve sıksa uygulama sunucusu ile dosya/nesne depolama hizmeti.

Her hizmet farklı bir konumda daha ucuz görünüyor diye bileşenleri kıtalar arasında dağıtmayın.

Harici bir bağımlılık belirli bir bölgeye bağlıysa iki yolu da ölçün:

1. kullanıcı → VPS;
2. VPS → bağımlılık.

Ardından iş yükünde hangi yolun daha belirleyici olduğuna karar verin.

## API'ler ve üçüncü taraf hizmetler en uygun konumu değiştirebilir {#apis-and-third-party-services-can-change-the-best-location}

Bazı iş yüklerinde asıl önemli hedef kullanıcı değildir.

Örnekler:

- sabit bir bölgedeki API'ye çok sayıda çağrı yapan uygulama;
- dünya genelinden kullanılan, ancak tek bir bölgesel veritabanına bağlı özel yönetim ekranı;
- çoğunlukla başka bir sunucuyla iletişim kuran otomasyon;
- sıkı yanıt süresi gereksinimleri olan ödeme veya stok entegrasyonları.

Uygulama her sayfa isteğinde aynı uzak bağımlılığa birkaç eşzamanlı çağrı yapıyorsa VPS'yi kullanıcılara yaklaştırmak tarayıcı yolunu kısaltırken uygulama yolunu uzatabilir.

İşlemin tamamını ölçün.

## CDN ve kaynak sunucunun konumu {#cdn-vs-origin-location}

CDN, konum kararını değiştirir; ancak kaynak sunucunun nerede bulunduğunu önemsiz hale getirmez.

CDN, önbelleğe alınabilen dosyaları kullanıcılara yakın noktalardan sunabilir:

- görseller;
- CSS;
- JavaScript;
- indirilebilir dosyalar;
- güvenli biçimde yapılandırıldığında önbelleğe alınabilen HTML.

Böylece bu isteklerin katettiği mesafe önemli ölçüde azalabilir.

Ancak aşağıdaki trafik türlerinde kaynak sunucu hâlâ önemlidir:

- oturum açma;
- sepet ve ödeme;
- hesap sayfaları;
- önbelleğe alınmayan CMS istekleri;
- kişiselleştirilmiş HTML;
- API çağrıları;
- önbellekte bulunmayan içerik istekleri;
- önbellek temizleme ve yeniden doldurma işlemleri;
- yönetim paneli trafiği.

Trafiğinin büyük bölümü statik içerikten oluşan küresel bir web sitesi, kullanıcıya aktarılan verinin çoğunu CDN sağlıyorsa daha merkezi bir kaynak sunucuyla çalışabilir. Dinamik isteklerin yoğun olduğu bir site için kaynak sunucunun konumu çok daha önemlidir.

Google da CDN'leri içeriği kullanıcılara daha yakın konumlardan sunarak gecikmeyi azaltmanın bir yolu olarak tanımlar. Bu, kaynak sunucunun mimariden çıktığı anlamına gelmez.

## CDN bütün bölgeleri eşdeğer hale getirmez {#a-cdn-does-not-make-every-region-equivalent}

Aynı CDN arkasındaki iki farklı kaynak sunucu bölgesi, gerçek kullanımda farklı performans gösterebilir.

Dinamik istekler kaynak sunucuya ulaşır. Önbellekte bulunmayan içerik istekleri kaynak sunucuya ulaşır. CDN de güncellenen içeriği kaynak sunucudan almak zorundadır.

Küresel bir kitle için şunları test edin:

- önbellekten sunulan sayfaların performansı;
- önbelleğe alınmayan sayfaların performansı;
- oturum açma, hesap ve API uç noktaları;
- kaynak sunucunun ilk bayta kadar geçen süresi (TTFB);
- içerik önbellekte bulunmadığında oluşan davranış.

Ana sayfa önbellekten hızlı açılıyor diye uzak bir kaynak sunucu seçmeyin.

## Küresel kitle: tek kaynak sunucu ve CDN mi, birden fazla bölge mi? {#global-audience-one-origin--cdn-or-multi-region}

Küresel bir kitleye sahip olmak, birden fazla VPS bölgesini kendiliğinden gerekli kılmaz.

### Tek kaynak sunucu ve CDN {#one-origin--cdn}

Aşağıdaki durumlarda bu genellikle daha basit bir başlangıç mimarisidir:

- içeriğin çoğu önbelleğe alınabiliyorsa;
- dinamik trafiği oluşturan en büyük veya en değerli kitle tek bir bölgedeyse;
- uygulama ve veritabanı durum bilgisi tutuyorsa;
- operasyon ekibi küçükse;
- uzaktaki dinamik kullanıcılar için küçük bir ek gecikme kabul edilebiliyorsa.

Kaynak sunucuyu en önemli dinamik trafik ve bağımlılıklara göre konumlandırın. Önbelleğe alınabilen içeriği dağıtmak için CDN kullanın.

### Birden fazla bölge gerekli olabilir {#multi-region-may-be-justified}

Uygulamayı birden fazla bölgede çalıştırmak şu koşullarda anlamlı olabilir:

- dinamik kullanıcılar farklı bölgelere yayılıyorsa;
- izin verilen gecikme süresi kısaysa;
- bölgesel yük devretme bir iş gereksinimiyse;
- uygulama dağıtık durum yönetimi için tasarlandıysa;
- veritabanları, kuyruklar ve oturumlar güvenle çoğaltılabiliyorsa;
- ekip birden fazla arıza alanını yönetebiliyorsa.

Birden fazla bölge ek karmaşıklık getirir:

- veri çoğaltma;
- yazma tutarlılığı;
- oturum yönetimi;
- önbellek geçersizleştirme;
- yük devretme;
- dağıtım koordinasyonu;
- izleme;
- maliyet.

Sağlayıcı sunuyor diye yeni bölgeler eklemeyin.

## İki bölgeye yayılan kitle için ağırlıklı bir karar verin {#two-region-audiences-need-a-weighted-decision}

Kitle iki bölgeye bölünmüşse üç yaygın yaklaşım vardır:

| Yaklaşım | Uygun olduğu durum |
|---|---|
| Kaynak sunucuyu daha büyük veya daha değerli kitleye yakın tutmak | dinamik trafik açısından bir bölge açıkça daha önemliyse |
| Ortada veya merkezi bir bölge ve CDN | dinamik trafik orta düzeydeyse ve her iki taraf için ağ yolu kalitesi kabul edilebiliyorsa |
| Birden fazla bölgede uygulama | iki tarafta da dinamik trafik önemliyse ve uygulama dağıtık durum yönetimini destekliyorsa |

Test etmeden coğrafi orta noktayı seçmeyin. İnternet yönlendirmesi, orta noktanın iki pazar için de en iyi yolu sağlayacağını garanti etmez.

## Fiziksel konum ve IP coğrafi konumu {#physical-location-vs-ip-geolocation}

Bir coğrafi konum veritabanı, IP adresini sunucu donanımının fiziksel olarak bulunduğu yerden farklı bir konumda gösterebilir.

Fiziksel konum önemliyse şunları doğrulayın:

- sağlayıcının belirttiği veri merkezi şehri veya bölgesi;
- hizmetin gerçek uç noktası;
- ağ yolunun özellikleri;
- gerekli olduğunda sözleşmedeki veri konumu ifadeleri.

Tek bir GeoIP sitesine bakarak fiziksel konum sonucuna varmayın.

GeoIP, uygulamalar, dolandırıcılık tespit sistemleri veya bölgeye göre sunulan hizmetler için önemli olabilir. Ancak bu, gerçek ağ gecikmesinden ayrı bir konudur.

## Yargı yetkisi ve verilerin tutulacağı yer {#jurisdiction-and-data-residency}

Konum seçimini performans dışındaki koşullar da sınırlayabilir.

Örneğin:

- sözleşmedeki veri yerleşimi gereksinimleri;
- mevzuata tabi müşteri verileri;
- şirket içi politikalar;
- müşterinin satın alma koşulları;
- sınır ötesi veri işleme veya depolama kısıtlamaları.

Böyle bir gereksinim varsa önce hukuken ve sözleşme açısından uygun bölgeleri belirleyin. Ardından bu bölgeler içinde performansı iyileştirin.

Bu sayfa hukuki danışmanlık sunmaz. Mevzuata veya sözleşmeyle belirlenen kısıtlamalara tabi veriler için gereksinimleri yetkin hukuk/uyum danışmanlığı ve sağlayıcının güncel sözleşme belgeleriyle doğrulayın.

## VPS konumu SEO'yu etkiler mi? {#does-vps-location-affect-seo}

Doğrudan sıralama artışı vaat ediliyor diye VPS'nin ülkesini seçmeyin.

Google'ın güncel açıklamasına göre sunucu konumu, sitenin hedef kitlesine ilişkin **bir sinyal olabilir**, ancak **kesin bir gösterge değildir**. Özellikle siteler CDN kullanabildiği veya altyapısı daha iyi ülkelerde barındırılabildiği için bu ayrım önemlidir.

Belirli bir bölgeyi açıkça hedeflemek için Google şu sinyallere işaret eder:

- dil veya bölgeye özel URL'ler;
- `hreflang`;
- uygun olduğunda ülke kodlu alan adları;
- açık bir bölge ve dil yapısı.

Bu nedenle:

**VPS konumunu öncelikle kullanıcılar, ağ yolları, bağımlılıklar ve operasyon/veri gereksinimlerine göre seçin; SEO için kestirme bir yol olarak görmeyin.**

Küresel bir site için hızlı ve güvenilir bir mimariyle doğru uluslararası hedefleme, yalnızca sıralama kazanmak amacıyla kaynak sunucuyu taşımaktan daha sağlam bir yaklaşımdır.

## Konum ve kaynak boyutlandırma ayrı kararlardır {#location-and-resource-sizing-are-separate-decisions}

Daha yakın bir sunucu, yetersiz CPU, RAM veya depolamayı telafi etmez.

Daha büyük bir VPS, ağ mesafesini ortadan kaldırmaz.

Bunları iki ayrı soru olarak değerlendirin:

1. **Sunucu nerede olmalı?** → Bu sayfa.
2. **Sunucunun kaynakları ne kadar olmalı?** → [Web sitesi için VPS kaynak seçimi]({{< relref "vps-sizing-for-website.md" >}}).

En uygun şehirdeki yanlış boyutlandırılmış bir sunucu yine yavaş olabilir. Yanlış ağ yolundaki güçlü bir sunucu da kullanıcılara yavaş gelebilir.

## Konum ve birden fazla web sitesi {#location-and-multiple-websites}

Birden fazla site barındıran VPS, farklı kitlelere hizmet verebilir.

Bütün siteler aynı pazara hitap ediyorsa konum seçimi daha kolaydır.

Müşteri siteleri farklı kıtaları hedefliyorsa tek VPS bir uzlaşma gerektirir: kitleleri farklı olsa da bütün siteler aynı kaynak sunucu bölgesini paylaşır.

Karma site portföylerini şu ölçütlerle sınıflandırın:

- kitlenin coğrafi dağılımı;
- dinamik trafik;
- iş açısından önem;
- uyum kısıtlamaları.

Bir sitenin konum gereksinimi belirgin biçimde farklıysa bütün siteleri aynı bölgeye zorlamak yerine o site için ayrı VPS kullanmak daha uygun olabilir.

Birlikte barındırma ve yalıtım kararı için [Birden fazla web sitesi için VPS]({{< relref "vps-for-multiple-websites.md" >}}) sayfasını kullanın.

## Arıza alanları da önemlidir {#failure-domains-matter-too}

Canlı sistem için en hızlı bölge, bütün destekleyici kopyaların da bulunması gereken yer değildir.

İş riskine göre kritik kurtarma ve izleme bağımlılıklarını aynı arıza alanından ayırmayı değerlendirin:

- sunucu dışındaki yedekler;
- harici erişilebilirlik kontrolleri;
- olay bildirimleri;
- ikincil kopyalar.

Amaç «her şeyi uzağa koymak» değildir. Tek bir bölge, sağlayıcı veya ağ arızasının hem canlı sistemi hem de arızayı tespit etmek veya sistemi kurtarmak için gereken araçları devre dışı bırakmasını önlemektir.

Kurtarma tasarımı için [VPS yedekleme stratejisi]({{< relref "vps-backup-strategy.md" >}}), bağımsız erişilebilirlik kontrolleri için [VPS izleme]({{< relref "vps-monitoring.md" >}}) sayfasını kullanın.

## Yanlış konumu seçerseniz ne olur? {#what-if-you-choose-the-wrong-location}

Daha sonra bölge değiştirmek, sağlayıcıya ve uygulamaya bağlı olarak kolay olabilir veya kesintiye yol açabilir.

Olası sonuçlar şunlardır:

- yeni bir VPS oluşturmak;
- dosyaları ve veritabanlarını kopyalamak;
- yeni bir IP adresi almak;
- DNS'i değiştirmek;
- güvenlik duvarını ve IP izin listelerini güncellemek;
- CDN kaynak sunucu ayarlarını değiştirmek;
- webhook hedeflerini veya güvenilen IP adreslerini güncellemek;
- TLS'yi ve harici entegrasyonları doğrulamak;
- geçiş için bir zaman aralığı planlamak.

Bu nedenle aday konumları canlıya geçmeden önce test etmek, bölge seçimini yalnızca açılır menüdeki bir seçenek olarak görmekten daha az maliyetlidir.

Geçişin nasıl yapılacağı için [Web sitesini VPS sunucuya taşıma]({{< relref "website-migration-to-vps.md" >}}) sayfasını kullanın.

## Uygulanabilir bir bölge seçimi süreci {#a-practical-region-selection-workflow}

### 1. Kaynak sunucuya duyarlı trafiği belirleyin {#1-map-origin-sensitive-traffic}

Şunları kaydedin:

- öne çıkan ülkeler ve şehirler;
- ödeme yapan müşterilerin yoğunlaştığı yerler;
- oturum açmış kullanıcı trafiği;
- yoğun saatlerdeki kullanıcı konumları;
- API istemcileri.

### 2. Bağımlılıkları belirleyin {#2-map-dependencies}

Uygulamanın eşzamanlı iletişim kurduğu bileşenlerin konumlarını kaydedin:

- veritabanı;
- Redis ve önbellek;
- nesne veya dosya hizmeti;
- ödeme hizmeti ve API;
- kurum içi sistemler;
- harici SaaS hizmetleri.

### 3. Zorunlu konum kısıtlamalarını uygulayın {#3-apply-hard-placement-constraints}

Geçerli bir sözleşme, mevzuat veya kurum içi politika gereksinimine aykırı olan konumları eleyin.

### 4. Uygun olabilecek bölgeleri kısa listeye alın {#4-shortlist-plausible-regions}

Coğrafyayı yalnızca kısa liste oluşturmak için kullanın.

### 5. Temsili ağlardan test edin {#5-test-from-representative-networks}

Tekrarlanan ölçümlerle gecikmeyi ve ağ yolu kalitesini karşılaştırın. Mümkünse kullanıcılar açısından önemli birden fazla internet servis sağlayıcısını dahil edin.

### 6. Dinamik uygulama davranışını test edin {#6-test-dynamic-application-behavior}

Yalnızca önbellekten sunulan ana sayfanın yüklenme süresine bakmayın.

### 7. Gereksinimi karşılayan en basit mimariyi seçin {#7-choose-the-simplest-architecture-that-satisfies-the-requirement}

Ölçümler veya iş gereksinimleri daha fazla karmaşıklığı haklı çıkarana kadar iyi seçilmiş tek kaynak sunucu ve CDN tercih edin.

### 8. Yayından sonra izleyin {#8-monitor-after-launch}

Dışarıdan ölçülen gerçek gecikmeyi, TTFB'yi, hataları ve kullanıcıya görünen hizmet durumunu doğrulayın. Satın alma öncesi test bir kanıttır; kalıcı garanti değildir.

## VPS konumu için satın alma öncesi kontrol listesi {#vps-location-pre-purchase-checklist}

| Kontrol | Başarı koşulu |
|---|---|
| Kitle | önemli kullanıcıların ve trafiğin bölgeleri biliniyor |
| İş önceliği | ödeme yapan, oturum açan ve yoğun saatlerdeki kullanıcılar belirlendi |
| Dinamik trafik payı | kaynak sunucuya duyarlı istekler anlaşıldı |
| Bağımlılıklar | veritabanı, API ve özel hizmet konumları biliniyor |
| Aday bölgeler | kısa liste trafik ve kısıtlamalara dayanıyor |
| Test uç noktası | sağlayıcının test noktası veya deneme sunucusu ölçülebiliyor |
| Tekrarlanan RTT ölçümü | aday ağ yolları birden fazla örnekle karşılaştırıldı |
| Ağ yolu kalitesi | belirgin dolambaçlı yollar ve kararsızlıklar incelendi |
| İnternet sağlayıcılarının kapsamı | önemli kullanıcı ağları testlerde temsil ediliyor |
| CDN | önbelleğe alınabilen ve dinamik trafik ayrıldı |
| Kaynak sunucu | dinamik trafiğin yolu kabul edilebilir durumda |
| Fiziksel konum | gerektiğinde sağlayıcının gerçek bölgesi ve şehri doğrulandı |
| GeoIP | fiziksel veri merkezi konumuyla karıştırılmıyor |
| Veri konumu | sözleşme ve uyum kısıtlamaları kontrol edildi |
| SEO | sunucunun ülkesinden kaynaklanan bir sıralama vaadi varsayılmıyor |
| Kurtarma | yedekleme ve izlemenin arıza alanı değerlendirildi |
| Taşıma | daha sonra taşınmanın bir operasyon değişikliği olduğu anlaşıldı |
| Boyutlandırma | CPU, RAM ve depolama ayrı seçildi |

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Güncel VPS yapılandırmalarını inceleyin</a>
</p>
<p><small>Açıklama: Editörün VDSina ile profesyonel bir ilişkisi vardır. Bu iş ortaklığı bağlantısı üzerinden sipariş verirseniz site komisyon kazanabilir. Sipariş vermeden önce sağlayıcının güncel konumlarını ve ağ bilgilerini doğrulayın; bu sayfa belirli bir VDSina konum envanteri sunmaz.</small></p>

## Teknik kaynaklar {#technical-references}

- Google Search Central — Çok bölgeli ve çok dilli siteleri yönetme
- Google Search Central — CDN'ler ve tarama

## Sık sorulan sorular {#faq}

### Hangi VPS konumunu seçmeliyim? {#which-vps-location-should-i-choose}

Gecikmeye duyarlı en büyük veya en değerli kitlenin yakınındaki bölgeden başlayın, ardından temsili ağlardan gerçek yönlendirmeyi doğrulayın. Veritabanı ve API bağımlılıklarıyla zorunlu veri konumu gereksinimlerini de hesaba katın.

### Bana en yakın VPS konumunu mu seçmeliyim? {#should-i-choose-the-vps-location-closest-to-me}

Yalnızca önemli kullanıcı sizseniz. Herkese açık bir web sitesi normalde yöneticiye göre değil, ziyaretçileri, müşterileri ve kritik bağımlılıklarına göre konumlandırılmalıdır.

### En yakın veri merkezi her zaman en hızlısı mı? {#is-the-closest-data-center-always-the-fastest}

Hayır. Fiziksel mesafe önemlidir; ancak peering ve yönlendirme nedeniyle biraz daha uzak bir bölge, belirli bir internet sağlayıcısına daha iyi performans sunabilir. Gerçek ağ yolunu test edin.

### Satın almadan önce VPS konumunu nasıl test edebilirim? {#how-do-i-test-a-vps-location-before-buying}

Sağlayıcının test IP adreslerini, test dosyalarını, looking glass aracını veya kısa süreli bir sunucuyu kullanın. Kullanıcılarınızı temsil eden ağlardan tekrarlanan ping/RTT ölçümlerini, MTR/traceroute sonuçlarını ve mümkünse HTTP sürelerini karşılaştırın.

### CDN, VPS konumunu önemsiz hale getirir mi? {#does-a-cdn-make-vps-location-irrelevant}

Hayır. CDN, önbelleğe alınabilen içeriği kullanıcılara yakın sunabilir. Ancak dinamik istekler, oturum açma, ödeme, API'ler, önbellekte bulunmayan içerikler ve kaynak sunucudan veri çekme işlemleri hâlâ kaynak sunucuya bağlıdır.

### Küresel bir web sitesinin VPS'si nerede olmalı? {#where-should-a-global-website-host-its-vps}

En büyük veya en değerli dinamik kitlenin yakınındaki tek kaynak sunucu ve CDN, çoğu zaman en basit başlangıçtır. Birden fazla bölge ancak dinamik istek gecikmesi, dayanıklılık gereksinimleri ve uygulama mimarisi ek karmaşıklığı destekliyorsa anlamlıdır.

### VPS, veritabanına yakın mı olmalı? {#should-the-vps-be-near-the-database}

Sık veri alışverişi yapan dinamik bir uygulama için genellikle evet. VPS kullanıcılara yakın olsa bile uygulama ile veritabanı arasındaki tekrarlanan bölgeler arası gidiş gelişler yanıt süresini belirleyebilir.

### VPS sunucusunun konumu Google sıralamasını iyileştirir mi? {#does-vps-server-location-improve-google-rankings}

Bunu doğrudan sıralama kazanmanın kestirme yolu olarak görmeyin. Google, sunucu konumunun dil veya bölge sinyali olabileceğini, ancak kesin olmadığını belirtir. Gerektiğinde dil/bölgeye özel URL'ler ve hreflang gibi açık uluslararası hedefleme yöntemlerini kullanın.

### IP coğrafi konumu ile sunucunun fiziksel konumu aynı mı? {#is-ip-geolocation-the-same-as-physical-server-location}

Hayır. GeoIP veritabanları bir adresi gerçek veri merkezi konumundan farklı gösterebilir. Fiziksel konum önemliyse ayrıca doğrulayın.

### Daha sonra başka bir VPS bölgesine geçebilir miyim? {#can-i-move-to-another-vps-region-later}

Genellikle evet; ancak yeni VPS veya IP adresi, veri taşıma, DNS değişiklikleri, izin listesi ve CDN güncellemeleri ile bir geçiş planı gerekebilir. Sonradan taşınma ihtimalini azaltmak için canlıya geçmeden önce test edin.
