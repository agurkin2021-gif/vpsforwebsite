---
title: "WebサイトのVPS移行"
description: "WebサイトをVPSへ移行する手順。現状の構成を把握し、新サーバーをテストして最終書き込みを管理。DNSを安全に切り替え、メール・SEO・切り戻し経路を維持します。"
image: "images/home/vps-for-website-hero.webp"
slug: "webサイトのvps移行"
---

WebサイトのVPS移行は、旧サーバーで公開を続けながら新サーバーを構築・テストすると安全に進めやすくなります。現状を把握し、移行先のスペックを選び、コピーと検証を行い、最後のデータ変更を管理します。DNSは最後に切り替え、旧環境を廃止できるまで両方を監視します。

このページは、ドメインと公開URL構造を変えない移行を想定しています。ドメインやパスも変える場合は、URL対応表と恒久リダイレクトを別の作業として計画してください。

ホスティング選び全体は、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[移行の流れ](#quick-migration-plan) · [切り替え前チェック](#migration-cutover-preflight) · [最終同期](#control-new-writes-and-the-final-sync) · [DNS切り替え](#switch-dns-deliberately) · [SEO確認](#preserve-seo-when-urls-stay-the-same) · [よくある質問](#faq)

## 移行の流れ {#quick-migration-plan}

計画的な移行は、次の順序で進めます。

1. **移行元を把握する。** アプリ、実行環境、DB、ファイル、DNS、メール、cron、ワーカー、Webhook、外部依存先を記録します。
2. **移行先のスペックを選ぶ。** 実際の負荷と移行作業の余裕から、CPU・RAM・ディスクを決めます。
3. **復元可能なバックアップを作る。** 移行元サーバー外にコピーを置き、必要なDBとファイルが実際に含まれるか確認します。
4. **VPSを並行して構築する。** トラフィックを移す前に、Web環境・パネルを導入し、アプリの要件を満たします。
5. **最初の全データをコピーする。** 旧サイトを公開したまま、ファイル転送とDBインポートを行います。
6. **非公開でテストする。** hostsファイルの上書き、管理されたプレビュー用ホスト名などを使い、DNS変更前に新サーバーを動作確認します。
7. **最終書き込みを管理する。** ストア、会員、フォームなど更新されるサイトでは、短い書き込み停止か、アプリに合う最終差分同期を計画します。
8. **DNSは最後に切り替える。** 移す必要のあるレコードだけを変え、メールと所有権確認のレコードを維持します。
9. **両サーバーを監視する。** アクセス、エラー、フォーム、注文、cron、Webhook、メール、HTTPS、検索クローラーを確認します。
10. **受け入れ確認後に旧環境を廃止する。** 切り戻し期間中は使える状態に保ちます。

すべての移行で停止ゼロを約束することはできません。実用上できるだけ短い中断に抑え、想定外のデータ損失を防ぐ計画的な切り替えを目指します。

## 実際に何を移すか決める {#define-what-is-actually-moving}

「サイトを移す」作業には、複数のシステムが含まれる場合があります。コピー前に対象範囲を決めます。

| 構成要素 | 移行前に確認する内容 |
|---|---|
| Webサイト・アプリ | CMS・フレームワーク、ドキュメントルート、アップロード、隠しファイル、キャッシュ、書き込み先 |
| 実行環境 | PHP・Node・Pythonのバージョン、拡張・モジュール、Webサーバー、プロセス管理 |
| データベース | エンジン・バージョン、サイズ、ユーザー・権限、文字セット、定期保守 |
| DNS | 提供元、A・AAAA・CNAME、www・ルートドメインの動作、TTL、確認用レコード |
| メール | 保存先、MX、SPF、DKIM、DMARC、メールボックス、転送、SMTP |
| 定期処理 | cron、キュー、ワーカー、インポート、エクスポート、バックアップ、予約処理 |
| 外部システム | 決済Webhook、API、IP許可リスト、CDN・WAF、解析、Search Console |
| セキュリティ・秘密情報 | 環境変数、APIキー、SSH鍵、TLS、ファイアウォールルール |

理由なく無関係な変更をまとめないでください。ドメイン、URL構造、アプリのバージョン、大きなソフトウェア更新を同時に変えなければ、移行時の原因調査がしやすくなります。

## 移行切り替え前チェック {#migration-cutover-preflight}

DNSを変える前に使ってください。移行の成功を保証するものではなく、先に解決すべき前提条件の不足を見つけます。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="migration-preflight">
  <div class="mb-6">
    <label for="mig-backup" class="form-label">独立したバックアップがあり、復元・インポートをテスト済み</label>
    <select id="mig-backup" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-sizing" class="form-label">移行先のCPU・RAM・ディスクを余裕込みで選定済み</label>
    <select id="mig-sizing" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-runtime" class="form-label">実行環境・DB・必要な拡張の互換性を確認済み</label>
    <select id="mig-runtime" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-test" class="form-label">DNS切り替え前に新サイトを非公開でテスト済み</label>
    <select id="mig-test" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-dns" class="form-label">DNSを記録し、TTLと切り替えを計画済み</label>
    <select id="mig-dns" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-mail" class="form-label">メールの保存先とMX・SPF・DKIM・DMARCの扱いを決定済み</label>
    <select id="mig-mail" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option><option value="na">対象外・メールは別環境で変更なし</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-writes" class="form-label">注文・フォーム・会員・アップロードの最終書き込みと同期を計画済み</label>
    <select id="mig-writes" class="form-input"><option value="no">未準備</option><option value="yes">準備済み・実質読み取り専用</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-tls" class="form-label">移行先で実際のホスト名を使ってHTTPS・TLSを利用できる</label>
    <select id="mig-tls" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-jobs" class="form-label">cron・ワーカー・Webhook・IP許可リストを記録し管理している</label>
    <select id="mig-jobs" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option><option value="na">対象外</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-rollback" class="form-label">切り戻し条件を決め、旧環境を利用可能なまま残す</label>
    <select id="mig-rollback" class="form-input"><option value="no">未準備</option><option value="yes">準備済み</option></select>
  </div>
  <button class="btn btn-primary" type="submit">切り替えの準備を確認</button>
</form>
<p id="migration-preflight-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">実際に準備できた項目を選んでください。</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("migration-preflight");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var items = [
      ["mig-backup", "独立したバックアップ"],
      ["mig-sizing", "移行先のスペック選定"],
      ["mig-runtime", "実行環境・DBの互換性"],
      ["mig-test", "移行先の非公開テスト"],
      ["mig-dns", "DNS・TTLの計画"],
      ["mig-mail", "メール・メール用DNSの計画"],
      ["mig-writes", "最終書き込み・データ同期の計画"],
      ["mig-tls", "HTTPS・TLSの準備"],
      ["mig-jobs", "cron・ワーカー・Webhook・許可リスト"],
      ["mig-rollback", "切り戻し計画"]
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
      result = "計画的な切り替えの準備完了：必要な項目はすべて準備済み、または明確に対象外とされています。DNSを変える直前に、最終同期と切り戻し条件を再確認してください。";
    } else {
      result = "切り替えの準備が未完了：先に次の不足を解消してください：" + missing.join(", ") + ".";
    }

    document.getElementById("migration-preflight-result").textContent = result;
  });
});
</script>

## 現在のWebサイトを棚卸しする {#inventory-the-current-website}

移行先を操作する前に、移行記録を作成します。

次を記録します。

- ドメインと稼働中の全サブドメイン。
- アプリ・CMS・フレームワークのバージョン。
- PHP、Node.js、Pythonなどの実行環境バージョン。
- DBエンジン・バージョン、サイズ、認証情報の管理方式。
- ドキュメントルートと、その外のディレクトリー。
- アップロード・メディアと書き込み可能なディレクトリー。
- リダイレクトと書き換えルール。
- cron、キュー、ワーカー、定期処理。
- 利用する場合はRedisなどのキャッシュサービス。
- SSL・TLS設定。
- DNSレコード。
- メールボックス、転送、送信SMTP経路。
- 決済ゲートウェイ、Webhook、APIコールバック。
- 外部サービスのIP許可リスト。
- CDN・WAF・オリジンへの接続制限。
- Search Console・解析の所有権確認。
- 現在のストレージ使用量と増加量。

この一覧は移行後の受け入れチェックにもなります。各項目がVPSで動作するか、意図的に外部サービスへ残されていることを確認します。

## 移行先VPSのスペックを選び、準備する {#size-and-prepare-the-destination-vps}

移行してから容量が足りるか考えるのは避けてください。

現在の処理負荷、DBの動作、ストレージ増加、パネル・メールの負荷、移行用の作業領域から選びます。移行中はアーカイブ、DBダンプ、ログ、バックアップの一時保存にもディスクが必要になる場合があります。

リソース計算は、[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})をご覧ください。

移行は管理方式を選ぶ機会でもあります。旧ホストでサーバー管理の多くが不要だったなら、まず切り替え後の担当を決めます。[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})を比較してください。その後、パネルを使うかLinuxを手動管理するかを決めます。[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})で説明しています。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">移行先のVPSを選ぶ</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で注文されると当サイトが報酬を受け取る場合があります。報酬によって移行手順やスペックの判断基準は変わりません。</small></p>

## 切り戻しに使えるバックアップを作る {#create-a-rollback-capable-backup}

必要なデータを含み、復元できてこそバックアップが役立ちます。

移行前に次を行います。

1. サイトファイルの新しいコピーを作る。
2. 必要なDBをすべてエクスポートする。
3. 移行元のホスティングアカウント外にコピーを置く。
4. 設定ファイルと環境変数を安全に記録する。
5. DNSとメールのレコードを別に記録する。
6. 可能なら使い捨て・テスト環境へ復元する。最低でも実際にDBをインポートし、代表的なファイルを確認する。アーカイブが開くことだけで済ませない。
7. 復元したコピーに期待するデータがあり、切り戻しに使える段階まで起動できることを確認する。
8. DNS変更前に切り戻し手順を書く。

動的サイトでは、最初のバックアップが本番の最終データではありません。コピー後も注文、フォーム、コメント、会員情報、アップロードが変わり続けます。最終差分は別に計画してください。

## DNS変更前に移行先を構築する {#build-the-destination-before-dns-changes}

公開トラフィックが来る前に、移行先でサイトを実行できるようにします。

次を一致させるか、意図的な違いを検証します。

- Webサーバーの動作。
- PHP・Node・Pythonのバージョン。
- 必要な拡張・モジュール。
- DBエンジン・バージョン。
- ファイル所有権と権限。
- アップロード・リクエスト本文のサイズ上限。
- 定期処理の実行環境。
- キャッシュサービス。
- 書き換え・リダイレクトルール。
- 環境変数と秘密情報。
- SMTP・外向き通信の要件。
- ファイアウォールルール。
- アプリ固有のパス。

必要な変更でない限り、移行と同時にすべての実行環境を更新したり構成を書き換えたりしないでください。同時変更を減らすと、切り戻しと原因調査がしやすくなります。

## ファイルとDBをコピーする {#copy-files-and-database}

転送方法は、移行元で使えるアクセス手段によって変わります。

代表的な方法は次のとおりです。

- cPanel・ファイルマネージャーとphpMyAdminのエクスポート。
- シェルが使えない場合はSFTP・FTP。
- 両側で許可されている場合はSSH・rsync。
- CMS固有の移行に対応するアプリケーション向けツール。
- 事業者のエクスポート・バックアップツール。

書き換えルールなど、アプリに必要な隠し設定ファイルを保持します。インポート後は、DBユーザー、権限、文字セット・照合順序の前提、アプリの接続設定を確認します。

大きなデータでは、可能な範囲でサイズ、行数、チェックサムを比較します。「転送完了」だけで同一データと判断しないでください。

## 切り替え前に非公開でテストする {#test-privately-before-cutover}

未検証のサーバーへDNSを向けないでください。

hostsファイルの上書き、管理されたプレビュー用ホスト名など、実際のアプリ構成を動かせる非公開の方法で移行先をテストします。

次を確認してください。

- ホームページと代表的な内部ページ。
- 管理者ログイン。
- ユーザーログイン。
- 画像、CSS、JavaScript、ダウンロード。
- 検索。
- フォームと送信結果。
- アップロード。
- リダイレクト。
- APIエンドポイント。
- 購入手続きと決済コールバック。
- cron・予約処理。
- キュー・ワーカー。
- メール送信。
- アプリ・Webサーバー・DBのログ。
- モバイル表示とナビゲーション。

一時的な公開ホスト名が、検索に重複ページとして登録されないようにします。テスト中に公開する場合はインデックスから除外し、本番ホスト名の一時的な制限は切り替え前に解除してください。

## 新規書き込みと最終同期を管理する {#control-new-writes-and-the-final-sync}

案内サイトと取引サイトで最も大きく異なる点です。

DNS切り替え中に旧・新の両DBが書き込みを受け付けると、データが分岐します。旧サーバーで保存された注文は、自動的に新サーバーへ現れるわけではありません。

データが変わるサイトでは、次を行います。

1. リスクの低い切り替え時間帯を選ぶ。
2. 可能な範囲で、移行元の新規書き込みを停止・制御する。
3. 二重に書き込む可能性のあるcron・キューワーカーを停止・制御する。
4. 最終DB同期を実行し、変更されたアップロード・ファイルをコピーする。
5. 正とする移行元データの最終時刻を記録する。
6. トラフィックを切り替える。
7. 新規書き込みが移行先だけに保存されることを確認する。

[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})では、購入手続き、注文、決済Webhook、在庫、予約処理、取引メールを受け入れテストに含めます。静的・キャッシュ中心のサイトなら、最終ファイル比較だけで足りる場合があります。

アプリと同期方法が実際に対応していない限り、停止ゼロの移行とは呼ばないでください。

## DNSを計画的に切り替える {#switch-dns-deliberately}

DNSはトラフィックを切り替える手段であり、移行の最初の作業ではありません。

切り替え前に次を行います。

- 現在のゾーンをエクスポート・記録する。
- 変更するA・AAAA・CNAME・オリジンのレコードを正確に特定する。
- 可能なら、旧TTLの期間が丸ごと経過する余裕を持ってTTLを短くする。例えば現在86,400秒なら、切り替えの24時間以上前に短くします。
- 今TTLを短くしても、以前の長いTTLで保存されたキャッシュは消えないことを理解する。
- 移行しないMX、SPF、DKIM、DMARC、確認用TXT、SRV、CAAなどのレコードを維持する。
- ルートドメインとwwwの両方の動作を確認する。

DNS事業者を変えないなら、通常はネームサーバー変更よりA・AAAAレコード変更のほうが低リスクです。ネームサーバーも変える場合は、先に必要なゾーン全体を再現してください。

切り替え後は複数のリゾルバー・ネットワークから公開DNSを確認し、アクセスが旧サーバーから新サーバーへ移る様子を監視します。

## メールを止めないために {#keep-email-from-breaking}

旧共用ホスティングで一緒に提供されていても、Webサイト移行とメール移行は別の作業です。

切り替え前に、次のいずれかを選びます。

- 現在の事業者・管理型メールに残し、既存のMX・TXTを維持する。
- 別の管理型メール事業者へ移す。
- VPSへメールを移し、メールボックス、振り分け、認証、到達性の対策を再構築する。

メールを移す場合は、次を考慮します。

- MXの優先順位。
- SPF。
- DKIM。
- DMARC。
- 必要に応じた逆引きDNS・PTR。
- メールボックスのデータ。
- エイリアス・転送。
- SMTP認証情報。
- 迷惑メールのフィルタリング。
- バックアップと送信元の評価。

メールやすべての依存先のレコードを再現せず、サイト移行だけのためにDNSゾーン全体を置き換えないでください。

## HTTPS・CDN・外部サービスを確認する {#verify-https-cdn-and-external-services}

移行先リージョンが未定なら、切り替え前に[VPSのリージョンの選び方]({{< relref "how-to-choose-vps-location.md" >}})で決めてください。後からリージョンを変えると、再びIP・DNS移行が必要になる場合があります。

IPアドレスで動く移行先でも、実際のホスト名では失敗する場合があります。

次を確認します。

- TLS証明書が必要なホスト名を含む。
- HTTP → HTTPSの転送が正しい。
- ルートドメイン ↔ wwwの正規化が変わっていない。
- HSTSの前提を理解している。
- CDN・WAFが新オリジンを指し、接続を許可する。
- プロキシを使う場合、実際のクライアントIPを正しく扱える。
- 決済Webhookが新オリジンに届く。
- 旧サーバーIPを許可していたAPI提供元の設定を更新した。
- SMTP・API認証情報が新サーバーから有効に使える。

一時的なファイアウォール・WAFの例外は狭く限定し、受け入れ確認後に削除します。

## URLを変えずにSEOを維持する {#preserve-seo-when-urls-stay-the-same}

ホスティングだけの変更なら、通常は公開URLを維持します。この場合のSEO作業は、主に**移行前後の状態をそろえること**です。

切り替え前後で次を比較します。

- HTTPステータスコード。
- canonical URL。
- robots.txt。
- meta robotsと意図しないnoindex。
- サイトマップのURL。
- 内部リンク。
- 重要な構造化データ。
- ページ内容と表示されるアセット。
- Search Consoleの所有権確認。
- Googlebotと通常利用者へのサーバー応答。

Google Search Centralでは、新ホスティングの準備・テスト、準備完了後のDNS変更、旧・新両環境の監視、アクセス移動後の旧環境廃止を推奨しています。DNS TTLを事前に短くし、Search Consoleの所有権確認を維持することも推奨しています。

ホスティング基盤だけを変え、ドメイン・URLを維持する場合、**Google Search Consoleのアドレス変更ツールは使いません**。これはドメイン移転用であり、同じURLのホスティング移行用ではありません。

ドメインやURLパスも変える場合は、旧・新URLの対応表と恒久的なサーバー側リダイレクトを用意します。同一URLでのVPS移行とは別のサイト移転作業です。

## 切り替えチェックリスト {#cutover-checklist}

DNS変更の直前に確認します。

| 確認項目 | 合格の条件 |
|---|---|
| バックアップ | 独立コピーがあり、復元・インポートと代表的なデータを確認済み |
| 移行先 | 実行環境、DB、権限、秘密情報が正しい |
| 非公開テスト | ページ、フォーム、ログイン、必要な購入手続き・APIが合格 |
| 最終データ | DB・アップロードの最終差分を反映し、正とする時刻を記録済み |
| 定期処理 | 旧cron・ワーカーを制御し、新処理を予定時刻に開始できる |
| DNS | 変更対象を特定し、メール・確認用レコードを維持 |
| HTTPS | 移行先が実際のホスト名を安全に配信できる |
| 外部サービス | Webhook、許可リスト、CDN・WAF、SMTPを確認済み |
| SEOの維持 | canonical・robots・サイトマップ・ステータスが意図どおり |
| 切り戻し | 発動条件、担当作業、旧環境の利用可能性を決定済み |

ファイルをコピーできたからではなく、移行先が受け入れ条件に合格したから切り替えます。

## 移行後の受け入れ確認と切り戻し {#post-migration-acceptance-and-rollback}

DNS変更後は、次を行います。

- 旧・新両サーバーのアクセス・エラーログを監視する。
- 新しいユーザー操作が移行先DBへ届くことを確認する。
- フォーム、購入手続き、ログイン、アップロードを再テストする。
- cron、キュー、予約処理を確認する。
- メール送信と、必要な場合は受信経路を確認する。
- CPU、RAM、ディスク、DBの動作を確認する。
- HTTPSとCDN・WAFの動作を確認する。
- 重要URLの200応答・リダイレクトが移行前と一致するか確認する。
- Search Consoleのクロール・インデックス状況を監視する。
- 合意した安定性確認期間中は旧環境を利用可能に保つ。

### 切り戻しではデータの境界に注意する {#rollback-has-a-data-boundary}

初期ならDNSを戻すだけで切り戻せる場合がありますが、**旧サーバーがまだ正しい最新データの保持元である間に限ります**。

新サーバーに注文、登録、コメント、アップロードが保存されると、DNSだけの切り戻しでは新しい変更を失う場合があります。その段階では、データの整合調整や計画した再同期が必要です。

移行前に、例えば次の切り戻し条件を決めます。

- 広範囲の5xxエラー。
- 購入手続き・決済の失敗。
- DB破損・書き込みの欠落。
- 深刻な実行環境の非互換性。
- 認証の故障。
- 合意した時間内に直せない、重要なメール・Webhookの失敗。

## WordPress・WooCommerce・独自アプリの注意点 {#wordpress-woocommerce-and-custom-application-notes}

### WordPress {#wordpress}

PHPバージョンと拡張、DB互換性、アップロード、書き換えルール、wp-cron、キャッシュ、SMTP・問い合わせフォーム、管理ログインを確認します。シリアライズ済みデータを壊す無条件の検索置換を避け、必要に応じてアプリ対応ツールを使ってください。

リソースの特性は、[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})をご覧ください。

### WooCommerceなどの取引サイト {#woocommerce-and-other-transactional-sites}

注文、在庫、決済コールバック、セッション、予約処理、取引メールを、変化し続ける本番データとして扱います。最初のコピーに頼らず、DBと書き込みの最終切り替えを計画してください。

[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})もご覧ください。

### 独自アプリケーション {#custom-applications}

環境変数、秘密情報、バックグラウンドワーカー、キュー、ビルド・実行環境のバージョン、オブジェクトストレージ、ファイルパス、Webhook、API許可リスト、デプロイ・起動動作を記録します。IP応答だけでなく、実際のホスト名でテストしてください。

## 技術資料 {#technical-references}

- Google Search Central：ホスティング変更とSEO
- Google Search Central：URL変更を伴うサイト移転

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">移行用のVPSを選ぶ</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があります。提携リンクにはsponsored属性を付けています。VPS料金、転送量などの条件は変わる場合があるため、注文前に最新の提供内容を確認してください。</small></p>

## よくある質問 {#faq}

### ドメインを変えずにVPSへ移行できますか？ {#can-i-migrate-a-website-to-a-vps-without-changing-the-domain}

はい。同じドメインと公開URLを維持できます。先に移行先を構築・テストし、その後DNSレコードを変えて新サーバーへトラフィックを送ります。

### VPS移行に301リダイレクトは必要ですか？ {#do-i-need-301-redirects-when-moving-a-website-to-a-vps}

公開URLが同じなら不要です。ドメイン、プロトコル、パス、コンテンツ構成などでURLが実際に変わる場合に必要です。

### VPS移行の停止時間を減らすには？ {#how-do-i-reduce-downtime-during-a-vps-migration}

移行先を並行構築し、関連するDNS TTLを事前に短くします。非公開テスト、最終書き込みの管理、最終同期を行い、受け入れ確認後にDNSを変更します。反映中は旧環境を残します。

### メールもVPSへ移すべきですか？ {#should-i-move-email-to-the-vps-too}

必須ではありません。管理型メールに残すと、移行と到達性のリスクを減らせる場合があります。移すならMX、SPF、DKIM、DMARC、メールデータ、必要な逆引きDNS、バックアップを別に計画してください。

### DNS変更前に何をテストすべきですか？ {#what-should-i-test-before-changing-dns}

代表的なページ、ログイン、フォーム、アップロード、検索、必要な購入手続き・決済コールバック、定期処理、API・Webhook、メール送信、HTTPS、リダイレクト、アプリ・サーバーログです。

### 移行後、旧ホスティングはどれだけ残すべきですか？ {#how-long-should-i-keep-the-old-hosting-after-migration}

DNSのアクセスが移り、新サーバーが安定し、新規書き込みを確認し、合意した切り戻し期間が過ぎるまで残します。一律の時間・日数ではなくログで判断してください。

### 注文を失わずWooCommerceを移行できますか？ {#can-i-migrate-woocommerce-without-losing-orders}

はい。ただし、古いDBコピー1つだけに頼ってはいけません。切り替え中の書き込みを管理し、アプリに合う最終同期を行って、注文・在庫変更が2つの書き込み可能なDBへ分かれないようにします。

### ホスティング移行はSEOに悪影響がありますか？ {#does-moving-hosting-hurt-seo}

URLを変えず、同じ内容、ステータスコード、canonical、クロール可能性を維持すれば、検索上の情報も維持できるはずです。移行後はSearch Consoleとサーバーログを監視してください。基盤変更中はクロール頻度が一時的に変わる場合があります。
