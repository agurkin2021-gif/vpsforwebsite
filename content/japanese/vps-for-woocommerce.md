---
title: "WooCommerce向けVPS"
description: "WooCommerce向けVPSを、購入手続きの同時処理、PHPワーカー、DB書き込み、Action Scheduler、外部連携、セール時の負荷から選定。管理方法も解説します。"
image: "images/home/vps-for-website-hero.webp"
slug: "woocommerce向けvps"
---

WooCommerce向けVPSは、キャッシュ済みブログのようには扱えない処理、つまり**カート、購入手続き、アカウント、注文、在庫、決済コールバック、スケジュール済みアクション、DBへの書き込み**に合わせて選びます。月間アクセス数や商品数だけでは、ストアに必要なサーバー性能は分かりません。

WordPress全般の負荷については[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})、サーバー選び全体の流れについては[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[構成の目安](#quick-answer) · [適性チェック](#woocommerce-vps-fit-checker) · [購入手続きの負荷](#checkout-and-account-traffic-stay-dynamic) · [データベース](#database-demand-and-hpos) · [定期実行処理](#action-scheduler-and-background-work) · [セール時のピーク](#size-for-sale-and-campaign-peaks) · [よくある質問](#faq)

## 構成の目安 {#quick-answer}

以下は現在のVDSina Standardプランを検討する際の出発点です。注文数や訪問者数を保証するものではありません。

| WooCommerceの用途・負荷 | 検討の出発点となる構成 | 主に確認する制約 |
|---|---:|---|
| 検証・テスト用ストア、またはごく軽量で取引の少ない構成 | **1 vCPU / 2 GB / 40 GB** | PHP、DB、バックグラウンドジョブが重なると、本番運用の余裕が小さい |
| 小規模事業のストア | **2 vCPU / 4 GB / 80 GB** | 購入手続きの同時処理、PHPワーカー、DB遅延、定期実行処理 |
| 負荷の高いストア、大きな商品カタログ・DB、多数の連携、セール時のピーク | **4 vCPU / 8 GB / 160 GB** | 継続的なCPU負荷、PHPの待ち行列、DBのワーキングセット、Action Scheduler、ストレージの増加 |
| 1台の8 GB VPSを超える取引負荷 | **構成を再検討** | 1台を増強するだけでなく、DB・ワーカー・サービスの分離や、より強力なクラウド・マネージド構成を検討 |

WooCommerceの公式スケーリング資料では、OPcache、CDN、永続キャッシュを利用するセルフホスト構成の基礎として、**1 vCPU＋少なくとも2 GB RAM**が示されています。これは検討の下限であり、本番ストアを継続して余裕をもって運用できるという約束ではありません。

VDSina Standard料金の再確認日：2026年10月13日。

- 1 vCPU / 1 GB / 10 GB / 月間転送量1 TB — **$0.07/日**。
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/日**。
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/日**。
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/日**。

実際の事業用ストアでは、**4 GBのほうが実用的な開始構成**になることが多いです。VPSはOS、DB、PHPワーカー、キャッシュ、バックグラウンドジョブを同時に動かし、運用上の余裕も確保する必要があります。

ソフトウェア構成全体の詳細な計算は、[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})をご覧ください。

## WooCommerceの動作要件と本番VPSの必要スペックは異なる {#woocommerce-requirements-are-not-production-vps-sizing}

WooCommerce 10.8+の現在の推奨サーバー要件は次のとおりです。

- **WordPress 6.9+**。
- **PHP 8.3+**。
- **MySQL 8.0+またはMariaDB 10.6+**。
- **HTTPS**。
- **WordPressのメモリ上限256 MB+**。
- WebサーバーにはApacheまたはNginxを推奨。

これらの値で分かるのは、**「WooCommerceのソフトウェア要件を満たしているか」**です。

次のことまでは分かりません。

- 必要なPHPワーカー数。
- VPS全体に必要なRAM容量。
- DBのワーキングセットがメモリに収まるか。
- 負荷がかかった際に購入手続きが待たされるか。
- スケジュール済みアクションが遅れていないか。
- バックアップやインポートが顧客の処理と競合するか。
- 決済・Webhook連携がリクエストを遅らせていないか。

**WordPress・PHPのメモリ上限256 MBは、VPS全体のRAMが256 MBでよいという意味ではありません**。サーバー全体ではLinux、Webサーバー、DB、PHPワーカー、キャッシュ、ジョブ、パネル・メール、余裕分も必要です。

## WooCommerce向けVPSの適性チェック {#woocommerce-vps-fit-checker}

検討の出発点として使ってください。ベンチマーク結果を保証するものではありません。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="woocommerce-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wc-stage" class="form-label">ストアの段階・事業上の重要度</label>
    <select id="wc-stage" class="form-input">
      <option value="test">テスト・公開前・事業への影響が小さい</option>
      <option value="small">稼働中の小規模ストア</option>
      <option value="business">事業上重要なストア</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-limits" class="form-label">現在のホスティングで、リソースの上限に繰り返し達するか、機能が不足していますか？</label>
    <select id="wc-limits" class="form-input">
      <option value="no">いいえ・未測定</option>
      <option value="yes">はい</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-external" class="form-label">主な障害・遅延の原因は、決済、配送、税計算、SMTPなどの外部サービスだと特定されていますか？</label>
    <select id="wc-external" class="form-input">
      <option value="no">いいえ・不明</option>
      <option value="yes">はい</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-checkout" class="form-label">購入手続き・アカウント操作の同時実行</label>
    <select id="wc-checkout" class="form-input">
      <option value="low">低い</option>
      <option value="medium">中程度</option>
      <option value="high">多い・キャンペーン時に集中する</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-catalog" class="form-label">商品カタログ・検索・絞り込みの負荷</label>
    <select id="wc-catalog" class="form-input">
      <option value="light">軽い</option>
      <option value="medium">中程度</option>
      <option value="heavy">大規模・クエリが多い</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-jobs" class="form-label">負荷の高いプラグイン、インポート、Webhook、定期購入、定期ジョブがありますか？</label>
    <select id="wc-jobs" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-db" class="form-label">データベース・注文の処理量</label>
    <select id="wc-db" class="form-input">
      <option value="small">小規模・少ない</option>
      <option value="medium">中程度</option>
      <option value="heavy">書き込み・クエリが多い</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-panel" class="form-label">同じVPSで管理パネルやメールも動かしますか？</label>
    <select id="wc-panel" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-spikes" class="form-label">セール・メール配信・販促による負荷の急増が定期的にありますか？</label>
    <select id="wc-spikes" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-operator" class="form-label">VPSを運用できる担当者はいますか？</label>
    <select id="wc-operator" class="form-input">
      <option value="no">いいえ</option>
      <option value="help">マネージドサービス・有料管理支援があれば対応可能</option>
      <option value="yes">はい</option>
    </select>
  </div>
  <button class="btn btn-primary" type="submit">WooCommerce向けVPSの適性を確認</button>
</form>
<p id="woocommerce-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">ストアの実際の処理負荷に最も近い項目を選んでください。</p>
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
      result = "外部サービス・アプリを先に診断：主な障害は、VPSのリソース以外に原因があると特定されています。CPUやRAMを追加する前に、決済ゲートウェイ、API、SMTP、外部連携の経路を修正・測定してください。";
    } else if (!limits && stage !== "business" && score <= 2) {
      result = "マネージド・共用環境でも対応できる可能性：VPSを必要とする制約はまだ実測されていません。実際のリソースや機能の不足が確認できるまでは、管理が簡単な環境を維持するか、先に最適化してください。";
    } else if (stage === "business" && operator !== "yes") {
      result = "管理代行・管理支援を利用：事業上重要なストアですが、サーバー運用を社内で全面的に担当する人がいません。自己管理のみのVPSを選ぶ前に、マネージドサービスや有料の管理代行を確保してください。";
    } else if (score <= 2) {
      result = "軽量な2 GB・小規模ストア向け：1 vCPU / 2 GB / 40 GBは、ごく軽量なストアの基本構成として検討できます。本番運用に適していると判断する前に、購入手続き、PHPワーカーのメモリ、DB遅延、スケジュール済みアクションを検証してください。";
    } else if (score <= 7) {
      result = "実用的な4 GBから検討：2 vCPU / 4 GB / 80 GBは、動的な購入手続き、DB書き込み、通常のバックグラウンド処理がある小規模事業のWooCommerceストアに、より余裕を持たせられます。";
    } else {
      result = "8 GBまたは構成の見直し：4 vCPU / 8 GB / 160 GBは、負荷の高いストアやセール時のピークを想定した開始構成として検討できます。DB、ジョブ、外部連携の負荷が大きい場合は、処理の分離や、より強力なマネージド・クラウド構成も検討してください。";
    }

    document.getElementById("woocommerce-vps-fit-result").textContent = result;
  });
});
</script>

## WooCommerceにVPSが必要になる場面 {#when-woocommerce-actually-needs-vps}

次の場合、WooCommerceストアにVPSを選ぶ理由があります。

- 共用サーバーで、必要な処理がCPU・メモリ・プロセス数・I/Oの上限に繰り返し達する。
- 実際の負荷で購入手続き・アカウント操作のリクエストが待ち行列に入る。
- DBのワーキングセットや書き込み負荷を、より細かく制御する必要がある。
- 拡張機能が、現在のホスティングでは許可されていないサービスを必要とする。
- Redis・Memcachedや独自のサーバー設定が必要。
- Action Scheduler・バックグラウンドジョブを、より確実に実行したい。
- 商品インポート、フィード、在庫同期が顧客のアクセスと競合する。
- PHP・実行環境・Webサーバーの独自設定が必要。
- ステージングや、ストア固有の運用制御が必要。

小規模で安定したストアを、マネージドWooCommerce・WordPress環境で十分にサポートできている場合、VPSのほうがよいとは限りません。

## マネージドWooCommerceホスティングが適する場面 {#when-managed-woocommerce-hosting-may-be-better}

次の場合、自己管理型VPSは適していません。

- OS・セキュリティ更新の担当者がいない。
- 購入手続きの稼働状況やサーバー通知を誰も監視していない。
- バックアップはあるが、復元を検証していない。
- 決済・注文の停止が事業に重大な影響を与える。
- チームが必要としているのはLinux管理ではなく、WordPress・WooCommerceの支援。
- 現在のマネージド環境で性能と拡張性を十分に確保できている。

VPSでは自由度が増える一方、責任を持って対応すべき障害の種類も増えます。

売上に直結するストアを自己管理サーバーに載せる前に、[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})を確認してください。

## 購入手続きとアカウント操作は動的処理のまま {#checkout-and-account-traffic-stay-dynamic}

WooCommerce公式のキャッシュ資料では、顧客固有の状態を含む**カート・マイアカウント・購入手続き**をページ全体のキャッシュから除外するよう案内しています。

つまり、売上に関わる特に重要なリクエストでは、引き続き次の処理が発生します。

- PHP。
- セッション・カートの処理。
- 配送・税計算の処理。
- 決済連携のコード。
- データベースの読み書き。
- 注文の作成。
- 在庫更新。
- フック・拡張機能。

そのため、キャッシュされた商品ページは速く表示できても、購入手続きでは待ち時間が発生することがあります。

商品カタログのキャッシュヒット率だけで、WooCommerceのスペックを選ばないでください。

## PHPワーカーと動的処理の同時実行数 {#php-workers-and-dynamic-concurrency}

WooCommerceの動的リクエストでは、PHPワーカー数が同時に実行できる処理数を左右します。

目安として、次の式を使えます。

**実行中の動的リクエスト数≈1秒あたりのキャッシュされないリクエスト数×処理時間**

ピーク時に購入手続き・アカウント・APIの応答が平均0.8秒かかり、PHPに毎秒5件の動的リクエストが届く場合、管理作業、Webhook、バックグラウンドジョブを加える前でも、約4個のワーカーが同時に使用中になります。

ワーカーはそれぞれメモリを消費します。RAMの配分を決めずに数を増やすと、DBのメモリ不足や、スワップ・OOMを招く場合があります。

次のように考えます。

**WooCommerceに必要なRAM＝OS＋Webサーバー＋DB＋キャッシュ＋PHPワーカー＋ジョブ＋管理パネル・メール＋余裕**

そのうえで、一般的なワーカー数の設定をそのまま流用せず、ワーカーの平均・ピーク時のメモリ使用量を確認してください。

## WooCommerceのキャッシュを正しく設定 {#cache-woocommerce-correctly}

WooCommerceでは、層ごとにキャッシュを設計する必要があります。

### ページ全体のキャッシュ {#full-page-cache}

キャッシュ可能な商品カタログやコンテンツページに役立ちます。

次のページを無条件にキャッシュ**しないでください**。

- カート。
- 購入手続き。
- マイアカウント。
- 顧客・セッション固有の応答。

WooCommerce公式のキャッシュ資料は、これらのページを明示的に除外しています。

### OPcache {#opcache}

コンパイル済みのPHPバイトコードをキャッシュし、繰り返しコンパイルする負荷を減らします。

### 永続オブジェクトキャッシュ {#persistent-object-cache}

RedisやMemcachedは、処理内容が適していれば、DBやオブジェクトの繰り返し処理を減らせます。

ページ全体のキャッシュに代わるものではなく、非効率なクエリも自動では改善しません。

### ブラウザー・CDN {#browser--cdn}

静的ファイルやエッジで配信できるコンテンツに役立ちます。

CDNは静的コンテンツのオリジンへのリクエストを減らせますが、動的な購入手続きやDB処理は残ります。

## データベース負荷とHPOS {#database-demand-and-hpos}

WooCommerceでは、一般的なキャッシュ中心のWordPressサイトより、DBの読み書きが多くなります。

重要なDB処理には、次のものがあります。

- 注文の作成・更新。
- 顧客・アカウントのデータ。
- 在庫の変更。
- 商品・カタログの参照。
- セッション。
- 拡張機能のメタデータ。
- レポート・分析。
- 検索・絞り込み。
- 定期実行ジョブ。

WooCommerceの**High-Performance Order Storage（HPOS）**は、専用テーブルに注文データを保存します。WooCommerce 8.2以降の新規インストールでは、標準で有効になっています。

HPOSは構成上の重要な改善ですが、次の対応が不要になるわけではありません。

- 拡張機能・独自コードの互換性確認。
- クエリ・インデックスの見直し。
- 十分なDBメモリの確保。
- ストレージの低遅延。
- 監視。
- 大きな変更前のステージング・テスト。

既存の大規模ストアでは、本番を切り替える前にHPOSへの移行と重要な操作をテストすることを、WooCommerceは推奨しています。

## Action Schedulerとバックグラウンド処理 {#action-scheduler-and-background-work}

WooCommerceは**Action Scheduler**を使って、次のようなバックグラウンドジョブを処理します。

- 注文通知。
- 決済関連の処理。
- Webhook。
- 定期購入・更新。
- 拡張機能のジョブ。
- インポート・同期。

WooCommerceでは、**WooCommerce > ステータス > 予約済みアクション（Scheduled Actions）**で確認できます。

次の状態に注意してください。

- 失敗したアクション。
- 予定時刻を過ぎたアクション。
- 解消されない保留ジョブの滞留。
- 長時間かかるジョブ。
- 顧客のアクセスが集中すると増え続けるキュー。

Action Schedulerは標準ではWordPressのスケジューリングに依存するため、確実な実行時刻が必要な場合はサーバー側のcronが役立ちます。

キャッシュされたページが速くても、定期実行キューに失敗があれば、ストアの運用に支障が出ます。

## 決済・Webhook・メール・外部連携 {#payments-webhooks-email-and-integrations}

VPSを増強しても、購入手続きのすべての不具合が直るわけではありません。

外部への依存には、次のようなものがあります。

- 決済ゲートウェイ。
- 税計算API。
- 配送API。
- 在庫・ERPの同期。
- CRM。
- 注文確認などのトランザクションメール。
- 不正検知。
- Webhook。
- 外部の検索機能・サービス。

遅延の発生元がVPSか、外部サービスかを測定してください。

次を監視します。

- 決済コールバックの失敗。
- Webhookの配信。
- メールキュー。
- APIのタイムアウト。
- 再試行・再試行間隔を延ばす処理の動作。
- Action Schedulerの失敗。

外部APIのボトルネックを解決するためにCPUを追加しないでください。

## 商品カタログ・検索・絞り込み {#catalog-search-and-filtering}

大きな商品カタログの負荷は、商品数が多いという理由だけで生じるわけではありません。

実際の負荷は次の処理から生じます。

- 複雑な検索・絞り込みクエリ。
- 属性・タクソノミーのクエリ。
- 商品ルックアップテーブル。
- バリエーション数。
- 価格・在庫のルール。
- SQLや外部呼び出しを追加する拡張機能。
- キャッシュされない利用者別の結果。

検索・絞り込みのエンドポイントは、通常の商品ページ閲覧と分けて測定します。

永続キャッシュで一部の繰り返しクエリを減らせても、DBやクエリの設計は引き続き重要です。

## セール・キャンペーンのピークに合わせて選ぶ {#size-for-sale-and-campaign-peaks}

WooCommerceのピーク負荷では、次の処理が同時に重なることがよくあります。

- メール配信・広告からのアクセス。
- 商品カタログの閲覧。
- カートへの追加。
- 購入手続き。
- 決済コールバック。
- 注文メール。
- 在庫更新。
- 管理画面・注文処理。
- Webhook。
- スケジュール済みアクション。
- アクセス解析・ログ記録。

平均的な日ではなく、**実際のピークを代表する時間帯**に合わせてスペックを選びます。

大きな販促施策の前に確認してください。

1. 本番を代表する購入手続きの負荷でテストする。
2. PHPワーカーに余裕があるか確認する。
3. DBの遅延と接続数を確認する。
4. Action Schedulerの滞留を確認する。
5. インポート・バックアップ・スキャンを停止するか、実行時刻をずらす。
6. 外部の決済・配送・税計算APIを確認する。
7. 開催中はログとリソース指標を監視する。

## ストレージ・バックアップ・ステージング {#storage-backups-and-staging}

WooCommerceのバックアップでは、ファイルと取引データの両方を保護します。

次を含めてください。

- WordPress・WooCommerceのファイル。
- アップロード・商品画像などのメディア。
- データベース・注文データ。
- 復旧に必要な設定・認証情報。
- プラグイン・テーマ・独自コード。
- 外部連携の設定。

### 取引データを考慮した復旧 {#transaction-aware-recovery}

継続的に注文が入るストアでは、バックアップ間隔が注文データの損失リスクを左右します。

DBバックアップが1日1回なら、最大1日分の新しい取引が、その復旧ポイントに含まれない場合があります。

手軽さではなく、許容できる**目標復旧時点（RPO）**からバックアップ間隔を決めます。

バックアップ構成の詳細は、[VPSのバックアップ戦略]({{< relref "vps-backup-strategy.md" >}})で解説します。

### ステージング {#staging}

可能な範囲で、PHP・WooCommerce・プラグイン・テーマ・HPOS・決済の変更を、本番反映前にステージングでテストします。

ステージング用のコピーにもディスクが必要で、DB・RAM・バックアップのリソースを使う場合もあります。容量計画に含めてください。

## 管理パネル・FASTPANEL・手動構築 {#control-panel-fastpanel-or-manual-stack}

WooCommerceは、手動管理のLinux VPSでも、ホスティング用管理パネルを使っても運用できます。

一般的なパネルの選び方は、[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})をご覧ください。

VDSinaでFASTPANELを使う方法は、[FASTPANEL対応VPS]({{< relref "fastpanel-vps-hosting.md" >}})をご覧ください。

Linux上に手動で構築する手順は、[VPSでWebサイトを公開する方法]({{< relref "how-to-host-a-website-on-vps.md" >}})をご覧ください。

管理パネルは日常作業を簡単にしますが、購入手続きの安定性、WooCommerce・プラグインの更新、DB調整、バックアップ、障害対応の責任を引き受けるものではありません。

## 稼働中のストア移行ではデータの切り替え時点を決める {#live-store-migration-has-a-data-boundary}

WooCommerceの移行は「ファイルとDBをコピーするだけ」ではありません。

ストアが稼働している間も、注文、在庫、カート、顧客、定期実行処理は変化します。

移行では次を行います。

- 先に移行先を構築してテストする。
- 最後の書き込みを管理する。
- DBとアップロードを最終同期する。
- 書き込み可能な本番ストアが2つ並行稼働し、データが食い違う状態を避ける。
- 決済・Webhookのエンドポイントを確認する。
- メール・DNSの設定を維持する。
- 切り戻し計画を用意する。

切り替え全体の手順は、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})をご覧ください。

## WooCommerce向けVPSを増強する判断材料 {#woocommerce-vps-upgrade-triggers}

測定で次の状態が確認できたら、増強や構成変更を検討します。

- PHPワーカーの待ち行列が繰り返し発生する。
- キャッシュ・クエリ・プラグインを最適化しても、CPUの飽和が続く。
- メモリ不足・スワップ・OOM。
- DBの遅延・ワーキングセットを保持するメモリの不足。
- 処理能力不足によるAction Schedulerの滞留・失敗。
- 実際に必要なピーク負荷で購入手続き・決済にエラーが発生する。
- ストレージの増加で安全な余裕が減る。
- バックアップ・インポート・スキャンが顧客の処理と競合する。
- 複数のストア・サービスが1台のVPSのリソースを奪い合う。

サーバーのリソースが正常なのに購入手続きが遅い場合は、VPSを増強する前に決済・API・プラグイン・DBの原因を調べてください。

## WooCommerce向けVPSの公開前チェックリスト {#woocommerce-vps-launch-checklist}

| 確認項目 | 合格の条件 |
|---|---|
| WooCommerceの実行環境 | 現在の互換性を満たすWordPress・PHP・DBとHTTPS |
| PHPのメモリ | WooCommerce・WordPressのメモリ上限を設定し、それとは別にVPS全体のRAMも十分に確保 |
| PHPワーカー | 本番を代表する購入手続き・アカウント操作の同時処理に対応 |
| ページキャッシュ | カート・購入手続き・アカウント・セッション固有の処理を除外 |
| オブジェクトキャッシュ・OPcache | 各層を意図して選び、Redis・Memcachedは有効な場合だけ使用 |
| データベース | 注文・商品カタログ・クエリの負荷を監視し、HPOS互換性を把握 |
| 定期実行処理 | 原因不明の失敗・期限超過の滞留がない |
| 決済 | テスト注文・決済・返金・Webhookが正常 |
| 在庫 | 変更後も整合性を維持 |
| メール | 注文確認などのメールが信頼できる経路で届く |
| バックアップ | ファイル・DB・直近の注文に対するRPO・復元手順を定義 |
| ステージング | 重要な更新を本番と分けてテスト可能 |
| 監視 | 外部からサイト・購入手続きを確認し、CPU・RAM・ディスク・DBを監視可能 |
| 再起動 | Web・PHP・DB・ジョブが自動で復帰 |
| ピーク | 本番を代表するセール・キャンペーン負荷で検証済み |

## 現在のWooCommerce向けVPS構成例 {#current-woocommerce-vps-examples}

以下のVDSina Standardプランは用途との対応例であり、ストアの処理能力を保証するものではありません。

| VPS | 検討を始める際に適した用途 | 再検討が必要になる場面 |
|---|---|---|
| 1 vCPU / 2 GB / 40 GB — $0.50/日 | 検証用・ごく軽量な小規模ストア・取引量を制御できる構成 | 事業上重要な購入手続き、重いプラグイン、多数のジョブ |
| 2 vCPU / 4 GB / 80 GB — $0.67/日 | 小規模事業のWooCommerce向けの実用的な開始構成 | 大きなセール負荷、大規模なDB・商品カタログ、多数の連携 |
| 4 vCPU / 8 GB / 160 GB — $1.34/日 | 負荷の高いストア・DB、PHP、バックグラウンド処理に余裕を確保 | 1台構成がボトルネックになり、障害の影響が集中する |

Standardの1 GBプランは、WooCommerceの通常の本番運用向けとしては提示していません。

VDSinaの現在のStandardページでは、表示されているテンプレート・アプリ一覧にWooCommerce専用のプリインストール済みアプリは**ありません**。ワンクリック導入を前提にせず、対応するWordPress環境、手動構築、管理パネルを利用してください。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のWooCommerce向けVPSを確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で申し込むと当サイトが報酬を受け取る場合があります。契約前に最新のVPS料金、テンプレート、管理パネルの提供状況を確認してください。</small></p>

## 技術資料 {#technical-references}

- WooCommerce：推奨サーバー要件
- WooCommerce開発者資料：スケーリング
- WooCommerce開発者資料：キャッシュプラグインの設定
- WooCommerce：予約済みアクション
- WooCommerce開発者資料：High-Performance Order Storage
- VDSina Standard VPS

## よくある質問 {#faq}

### WooCommerceをVPSで動かすにはRAMがどれくらい必要ですか？ {#how-much-ram-does-woocommerce-need-on-a-vps}

一律の容量はありません。WooCommerce公式のスケーリング資料では、セルフホストの基礎構成として2 GBが示されています。ただし、PHPワーカー、DB、キャッシュ、ジョブを同居させる多くの事業用ストアでは、4 GB VPSのほうが余裕のある実用的な開始構成です。

### WooCommerceに2 GB RAMで十分ですか？ {#is-2-gb-ram-enough-for-woocommerce}

ごく小規模で軽量なストアや、取引量を制御できる構成なら足りる場合があります。本番運用に適していると判断する前に、購入手続きの同時処理、DB遅延、定期実行処理、メモリ使用状況を検証してください。

### WooCommerceに4 GB RAMで十分ですか？ {#is-4-gb-ram-enough-for-woocommerce}

多くの小規模事業のストアでは4 GBが実用的な出発点です。アクセスが多い場合、大きな商品カタログ・DB、多数の連携、定期購入、インポート、セール時の急増がある場合は、より多く必要になることがあります。

### WooCommerceは通常のWordPressよりなぜ重いのですか？ {#why-is-woocommerce-heavier-than-normal-wordpress}

カート、購入手続き、アカウント、注文、在庫、多くの連携機能が動的に処理されるためです。公開の商品カタログやコンテンツがキャッシュされていても、これらのリクエストではPHPとDBの処理が発生します。

### WooCommerceの購入手続きをキャッシュできますか？ {#can-i-cache-woocommerce-checkout}

カート、購入手続き、マイアカウントには顧客固有の状態が含まれるため、ページ全体のキャッシュから除外してください。他のキャッシュ層は、適したデータやコンテンツに使用します。

### WooCommerceにRedisは必要ですか？ {#does-woocommerce-need-redis}

必須ではありません。処理内容が適していれば、RedisやMemcachedで永続オブジェクトキャッシュを利用できます。ただし、正しいページキャッシュの除外設定や効率的なクエリに代わるものではありません。

### HPOSとは何ですか？ {#what-is-hpos}

High-Performance Order Storageは、WooCommerceの注文を専用テーブルに保存する仕組みです。WooCommerce 8.2以降の新規インストールでは標準で有効です。既存ストアで変更する際は、拡張機能・独自コードの互換性と重要な操作をテストしてください。

### WooCommerceの予約済みアクションとは何ですか？ {#what-are-woocommerce-scheduled-actions}

Action Schedulerが管理する、キューに入ったバックグラウンドジョブです。注文通知、決済関連処理、Webhook、拡張機能のタスクなどに使われます。失敗や期限超過によるキューの滞留は、運用上の問題を示す指標です。

### VDSinaにはWooCommerceがプリインストールされていますか？ {#does-vdsina-include-woocommerce-preinstalled}

現在のVDSina Standardページでは、表示されているテンプレート・アプリ一覧に、WooCommerce専用のプリインストール済みアプリはありません。利用できるテンプレートは実際の申込画面で確認してください。

### WooCommerceでは、常にVPSのほうがマネージドホスティングより優れていますか？ {#is-a-vps-always-better-for-woocommerce-than-managed-hosting}

いいえ。VPSは自由度やリソースが必要で、サーバーを運用できる場合に役立ちます。事業上重要なストアで社内にサーバー管理担当がいない場合は、マネージドWooCommerce・WordPressホスティングのほうが安全に運用できることがあります。
