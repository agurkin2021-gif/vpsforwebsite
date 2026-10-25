---
title: "WordPress向けVPS"
description: "WordPress向けVPSのCPUとRAMを、PHPワーカー、DB負荷、キャッシュ、プラグイン、バックグラウンド処理から選定。管理方法と移行手順も解説します。"
image: "images/home/vps-for-website-hero.webp"
slug: "wordpress向けvps"
---

WordPress向けVPSは、共用サーバーでは得られない自由度、環境の分離、サーバー機能が必要な場合に役立ちます。スペックは月間訪問者数ではなく、**キャッシュされないPHP処理、データベース負荷、プラグイン、バックグラウンドジョブ、ストレージの増加、WordPressと同居するサービス**を基準に選びましょう。

サーバー選び全体の考え方は、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[構成の目安](#quick-answer) · [適性チェック](#wordpress-vps-fit-checker) · [PHPワーカー](#php-workers-and-ram) · [キャッシュ](#wordpress-caching-layers) · [データベース](#database-demand) · [WP-Cron](#wp-cron-and-background-jobs) · [よくある質問](#faq)

## 構成の目安 {#quick-answer}

以下は現在のVDSina Standardプランを検討する際の出発点です。対応できる訪問者数を保証するものではありません。

| WordPressの用途・負荷 | 検討の出発点となる構成 | 主に確認する制約 |
|---|---:|---|
| 検証・テスト用、またはごく軽量なキャッシュ中心のWordPress | **1 vCPU / 1 GB / 10 GB** | RAMとストレージの余裕が非常に小さく、本番運用の標準構成にはしない |
| キャッシュが十分に効く小規模なWordPressサイト | **1 vCPU / 2 GB / 40 GB** | PHPワーカー、DBメモリ、プラグイン・バックグラウンド処理の負荷 |
| 企業のWordPressサイト | **2 vCPU / 4 GB / 80 GB** | キャッシュされない同時処理、DBの遅延、cron・プラグイン |
| 動的処理が多いWordPress、大きなDB、複数の稼働サイト | **4 vCPU / 8 GB / 160 GB** | 継続的なCPU負荷、PHPの待ち行列、DBのワーキングセット、ジョブの重複 |

VDSina Standard料金の再確認日：2026年10月13日。

- 1 vCPU / 1 GB / 10 GB / 月間転送量1 TB — **$0.07/日**。
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/日**。
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/日**。
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/日**。

カート、購入手続き、アカウント、注文、在庫を動的に処理するストアでは、キャッシュ中心の一般的なWordPressサイトと同じに扱わず、[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})を参照してください。

ソフトウェア構成全体のリソースを詳しく計算するには、[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})をご覧ください。

## WordPressの動作要件とVPSの必要スペックは異なる {#wordpress-requirements-are-not-vps-sizing}

WordPress.orgは現在、次の要件を満たすホスティング環境を推奨しています。

- **PHP 8.3以上**。
- **MariaDB 10.11+またはMySQL 8.0+**。
- **HTTPS**。
- WebサーバーにはApacheまたはNginxを推奨。

この要件で分かるのは、**「WordPressを動かせるか」**です。**「本番の処理負荷にどれだけのVPSリソースが必要か」**までは分かりません。

本番VPSでは、次の用途にもRAM・CPU・ストレージが必要です。

- Linux。
- Nginx・Apache。
- PHP-FPMワーカー。
- MySQL・MariaDB。
- OPcache。
- 使用する場合はページキャッシュ・オブジェクトキャッシュ。
- 管理パネル。
- 同じサーバーで運用する場合はメール。
- バックアップ。
- cronジョブ。
- マルウェア・セキュリティスキャン。
- インポート・エクスポート。
- 監視。
- 運用上の余裕。

WordPressのソフトウェア要件を、そのまま本番サーバーの推奨スペックと捉えないでください。

## WordPress向けVPSの適性チェック {#wordpress-vps-fit-checker}

このチェックは検討の出発点です。CPU・RAM・データベースの実測に代わるものではありません。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="wordpress-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wp-limits" class="form-label">現在のホスティングで、必要な処理が繰り返し上限に達するか、機能が不足していますか？</label>
    <select id="wp-limits" class="form-input">
      <option value="no">いいえ・未測定</option>
      <option value="some">時々リソースが不足する</option>
      <option value="yes">繰り返し上限に達する・VPSでしか使えない機能が必要</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-type" class="form-label">WordPressサイトの用途</label>
    <select id="wp-type" class="form-input">
      <option value="content">キャッシュ中心のコンテンツ・案内サイト・ブログ</option>
      <option value="business">フォーム・プラグイン・管理作業がある企業向けCMS</option>
      <option value="membership">会員制・ログイン・個別表示のサイト</option>
      <option value="store">WooCommerce・取引を行うストア</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-dynamic" class="form-label">キャッシュされないPHP・管理画面・APIの処理負荷</label>
    <select id="wp-dynamic" class="form-input">
      <option value="low">低い</option>
      <option value="medium">中程度</option>
      <option value="high">高い</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-jobs" class="form-label">負荷の高いプラグイン、インポート、スキャン、バックアップ、バックグラウンドジョブがありますか？</label>
    <select id="wp-jobs" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-db" class="form-label">データベースの規模・処理量</label>
    <select id="wp-db" class="form-input">
      <option value="small">小規模・少ない</option>
      <option value="medium">中程度</option>
      <option value="large">大規模・クエリが多い</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-panel" class="form-label">同じVPSで管理パネルやメールも動かしますか？</label>
    <select id="wp-panel" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-sites" class="form-label">稼働中のWordPressサイト数</label>
    <select id="wp-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">WordPress向けVPSの適性を確認</button>
</form>
<p id="wordpress-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">可能な限り、実際の負荷データを基に選択してください。</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("wordpress-vps-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var limits = document.getElementById("wp-limits").value;
    var type = document.getElementById("wp-type").value;
    var dynamic = document.getElementById("wp-dynamic").value;
    var jobs = document.getElementById("wp-jobs").value === "yes";
    var db = document.getElementById("wp-db").value;
    var panel = document.getElementById("wp-panel").value === "yes";
    var sites = document.getElementById("wp-sites").value;

    var score = 0;
    if (type === "business") score += 2;
    if (type === "membership") score += 4;
    if (type === "store") score += 5;
    if (dynamic === "medium") score += 2;
    if (dynamic === "high") score += 4;
    if (jobs) score += 2;
    if (db === "medium") score += 1;
    if (db === "large") score += 3;
    if (panel) score += 1;
    if (sites === "few") score += 2;
    if (sites === "many") score += 4;

    var result;

    if (limits === "no" && type === "content" && dynamic === "low" && score <= 1) {
      result = "現状維持・先に最適化：現時点ではVPSが必要だという明確な根拠がありません。実際の制限や必要なサーバー機能が明らかになるまでは、適切な共用サーバーやマネージドWordPressホスティングのほうが手軽な場合があります。";
    } else if (type === "store") {
      result = "WooCommerce向けの選定：購入手続き、アカウント、注文の動的処理を測定したうえで、4 GB RAM前後またはそれ以上を起点に検討してください。詳しくはWooCommerce向けVPSガイドを参照してください。ストアの通信は、キャッシュ中心の一般的なWordPressサイトとは異なります。";
    } else if (score <= 2) {
      result = "軽量構成の2 GBから検討：1 vCPU / 2 GB / 40 GBは、キャッシュが十分に効く小規模なWordPressサイトに適する場合があります。PHPワーカーとDBのメモリ、プラグインやバックグラウンドジョブの負荷を監視してください。";
    } else if (score <= 7) {
      result = "実用的な4 GBから検討：2 vCPU / 4 GB / 80 GBなら、企業のWordPressサイトで、PHPワーカー、データベース、キャッシュ、日常的なバックグラウンド処理により余裕を持たせられます。";
    } else {
      result = "8 GBまたは構成の見直し：4 vCPU / 8 GB / 160 GBは、動的処理が多いサイトや複数のWordPressサイトの開始構成として検討できます。一つのサイトやジョブがリソースを占有する場合は、VPSの増強だけでなく処理の分離も検討してください。";
    }

    if (limits === "no" && type !== "store" && score > 1) {
      result += " 現在のホスティングが実際の制約になっていない場合は、移行前に最適化して測定してください。";
    }

    document.getElementById("wordpress-vps-fit-result").textContent = result;
  });
});
</script>

## WordPressにVPSが必要になる場面 {#when-wordpress-actually-needs-vps}

アクセス数が非常に多くなくても、WordPressにVPSが適する場合があります。

主な理由は次のとおりです。

- 必要な処理によってCPU・メモリ・プロセス数の上限に繰り返し達する。
- 独自のPHP・実行環境の設定が必要。
- Redis・Memcachedなどのサーバー側サービスが必要。
- 訪問者のアクセスをきっかけにする処理ではなく、OSのcronで定期実行したい。
- 長時間動くバックグラウンドジョブがある。
- Nginx・Apacheの動作を独自に設定したい。
- 複数サイトを一つの管理下に置きたい。
- 処理やアカウントをより強く分離したい。
- サーバーレベルの監視やファイアウォールが必要。

症状が「サイトが遅い」だけなら、まず[VPSと共用サーバーの違い]({{< relref "vps-vs-shared-hosting.md" >}})を確認し、WordPress自体がボトルネックになっていないか調べてください。

## WordPressにVPSが不要な場面 {#when-wordpress-does-not-need-vps}

次の場合は、適切な共用サーバーやマネージドWordPressホスティングを継続できます。

- サイトが軽量で安定している。
- キャッシュが機能している。
- ホスティングのリソース指標で、繰り返し上限に達していない。
- 独自サービスやroot権限が不要。
- チームでLinuxの保守を担当したくない。
- 事業者によるバックアップ、セキュリティ、更新、ステージングの対応で十分。
- VPSに移しても、手軽なホスティングを運用作業の多い環境に置き換えるだけになる。

VPSなら必ず速くなるわけではありません。スペックや設定が不適切なVPSでは、良質なマネージド環境よりWordPressの動作が悪くなることもあります。

## PHPワーカーとRAM {#php-workers-and-ram}

キャッシュされないリクエストでは、PHP-FPMワーカー数が同時処理の主な上限になります。

稼働中の各ワーカーは、リクエストを処理する間メモリを使います。ワーカーを増やすと同時に処理できる動的リクエストも増えますが、RAMの割り当てを増やさずにワーカー数だけを増やすと、次の問題を招きます。

- スワップの発生。
- メモリ不足。
- OOMによるプロセスの強制終了。
- データベースに必要なメモリの不足。
- サーバーの不安定化。

実用的には、次のように考えます。

**WordPressに必要なRAM＝OS＋Webサーバー＋データベース＋キャッシュ＋PHPワーカー＋管理パネル・メール・ジョブ＋余裕**

そのうえで、次を計算します。

**PHPワーカーの目安数＝PHPに安全に割り当てられるRAM÷実測したワーカー1個あたりの平均メモリ使用量**

MySQL・MariaDB、キャッシュ、OSのメモリが残らなくなるような、理論上の最大ワーカー数を設定しないでください。

ログイン中の利用者、wp-admin、REST・APIリクエスト、検索、フォーム、プレビュー、個別表示ページは、ページ全体のキャッシュを通らず、PHPワーカーを使いやすい処理です。

## WordPressのキャッシュの種類 {#wordpress-caching-layers}

キャッシュには複数の層があります。

| 種類 | キャッシュする対象 | 主な効果 |
|---|---|---|
| **PHP OPcache** | コンパイル済みのPHPバイトコード | リクエストごとにPHPスクリプトを再コンパイルする処理を省く |
| **ページキャッシュ** | 生成済みのHTML | ログインしていない利用者への表示でWordPress・PHPの処理を省ける |
| **永続オブジェクトキャッシュ** | 再利用できるオブジェクトやクエリ結果 | データベースやアプリの繰り返し処理を減らす |
| **ブラウザー・CDNキャッシュ** | 静的コンテンツやエッジで配信できる内容 | オリジンの繰り返し転送やリクエストを減らす |

WordPress公式の最適化資料でも、キャッシュは重要な性能改善手段とされています。ただし、それぞれの層が解決する問題は異なります。

Redisをページキャッシュと混同しないでください。Redisは一般に永続オブジェクトキャッシュの保存先として使われ、ページ全体のキャッシュとは別の層です。

## 永続オブジェクトキャッシュとRedis {#persistent-object-cache-and-redis}

WordPressにはオブジェクトキャッシュAPIがありますが、標準のキャッシュは**リクエストをまたいで保持されません**。

永続化するには、RedisやMemcachedなどの外部バックエンドと、それに対応したWordPressの連携機能・ドロップインが必要です。

重いデータベース・オブジェクト処理を繰り返すサイトでは有効な場合がありますが、導入するだけで必ず速くなるものではありません。

Redisを追加する前に確認します。

- サイトやDBの処理内容で効果が見込めるか。
- PHPとデータベース用のRAMが十分に残るか。
- ヒット率とメモリ使用量を監視できるか。
- ページキャッシュは別途検討しているか。

ページ全体のキャッシュが効き、DB処理が軽いサイトでは、動的な会員サイトやクエリが多いサイトほどRedisの効果が出ない場合があります。

## データベースに必要なリソース {#database-demand}

WordPressでは、CPUが明らかに飽和する前にデータベースが性能の制約になることがあります。

次を確認してください。

- 遅いクエリ。
- 大きなoptionsデータや自動読み込みデータ。
- プラグインのメタデータ。
- 検索・絞り込み・レポートのクエリ。
- postmetaを多用する処理。
- データベースのワーキングセット。
- 同時書き込み。
- インポート・エクスポート。
- ストレージの遅延。

CPUを増やしても、非効率なクエリ自体は直りません。DBが大きなワーキングセットを必要とする場合、RAM増設は役立ちますが、インデックス、クエリ、プラグインの改善に代わるものではありません。

まず測定し、その後に増強します。

## プラグイン・テーマ・バックグラウンドジョブ {#plugins-themes-and-background-jobs}

プラグインが消費するのはディスク容量だけではありません。

プラグインやテーマによって、次の負荷が増える場合があります。

- PHP処理。
- データベースクエリ。
- 外部API呼び出し。
- 定期実行タスク。
- キャッシュの無効化。
- 管理画面のAJAX処理。
- 画像処理。
- セキュリティスキャン。
- バックアップ。
- インポート・エクスポート。
- アクセス解析・ログ記録。

重いタスクが、利用者のアクセス処理と重なる場合があります。

可能な範囲で、バックアップ、スキャン、インポート、画像処理はアクセスのピークを避けて実行しましょう。特定のプラグインやジョブが負荷の急増を招いている場合は、VPSのスペック不足と判断する前に修正や実行時刻の調整を行います。

## WP-Cronとバックグラウンドジョブ {#wp-cron-and-background-jobs}

WP-CronはOSのスケジューラーのように常時動く仕組みではなく、WordPressへのリクエストをきっかけに起動します。

通常のサイトではこれで十分な場合があります。実行時刻が重要な処理や高負荷の環境では、WordPress公式の開発者資料で説明されているように、OSのスケジューラーから決まった間隔でWordPressのcronを呼び出せます。

OSのスケジューラーへ切り替える場合は、次の順序で進めます。

- まず代わりの起動設定を作成する。
- 正常に動作することを確認する。
- 通常のアクセスによるWP-Cron起動を停止する方針なら、その確認後に無効化する。
- 失敗したジョブを記録し、監視する。

代わりのスケジューラーを用意せずにWP-Cronを無効化しないでください。

## ストレージ・メディア・ステージング・バックアップ {#storage-media-staging-and-backups}

ディスク容量には、WordPress本体以外も含めて見積もります。

次の領域を確保してください。

- アップロード・メディア。
- データベース。
- プラグイン・テーマ。
- ログ。
- キャッシュファイル。
- 更新用の一時ファイル。
- 画像処理用の一時領域。
- ステージング用のコピー。
- サーバー外へ転送するまでのバックアップアーカイブ。
- 今後の増加分。

現在20 GBを使うサイトでも、複製、復元、プラグイン更新、バックアップ圧縮の際には、一時的に大幅な追加容量が必要になる場合があります。

バックアップの唯一のコピーをVPS内に置かないでください。

## 手動管理・管理パネル・FASTPANELの選び方 {#manual-control-panel-or-fastpanel}

WordPressはcPanelなどの管理パネルがなくても正常に運用できます。

### Linuxを手動で管理 {#manual-linux}

次を重視する場合に適しています。

- 必要最小限のソフトウェア構成。
- SSHによる管理。
- Nginx・Apache・PHP・データベースの独自設定。
- 自動化やGitを使ったデプロイ。

手動で公開する手順は、[VPSでWebサイトを公開する方法]({{< relref "how-to-host-a-website-on-vps.md" >}})をご覧ください。

### 一般的な管理パネル {#generic-control-panel}

ドメイン、SSL、PHP、DB、ユーザー、メール、バックアップをブラウザーで管理することで、繰り返し作業を十分に減らせる場合に役立ちます。

[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})をご覧ください。

### FASTPANEL {#fastpanel}

FASTPANELの公式手順にはWordPressサイトの作成方法があります。VDSinaでは現在、設定済みパネルの選択肢としてUbuntu 22上のFASTPANELを案内しています。

FASTPANELを使う構築方法とスペック選定は、[FASTPANEL対応VPS]({{< relref "fastpanel-vps-hosting.md" >}})をご覧ください。

管理パネルは作業を簡単にしますが、導入してもVPSがマネージドサービスになるわけではありません。

## WordPress向けVPSの管理委託と自己管理 {#managed-vs-self-managed-wordpress-vps}

自己管理型VPSでは、次の作業を誰かが担当する必要があります。

- OS・パッケージの更新。
- SSH・ファイアウォールの管理。
- PHP・Webサーバーの更新。
- データベースの管理。
- WordPress・プラグイン・テーマの更新。
- バックアップと復元テスト。
- 監視。
- 障害対応。

担当者がいない場合は、WordPressや管理パネルがサーバーを管理してくれると考えず、管理代行を選んでください。

[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})をご覧ください。

## WooCommerceは通常のWordPressとは負荷が異なる {#woocommerce-is-a-different-wordpress-workload}

WooCommerceはWordPressと同じソフトウェア基盤を使いますが、実際のストアのアクセスでは異なる負荷特性を示します。

カート、購入手続き、アカウント、注文、在庫、多くのスケジュール済みアクションは動的処理です。ログインしていない利用者向けのキャッシュ済みブログページと同じには扱えません。

ストアの取引が重要な場合は、[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})で専用のスペック選定と運用方法を確認してください。

## 複数のWordPressサイト {#multiple-wordpress-sites}

複数のWordPressサイトでは、次のリソースや運用条件を共有します。

- CPU。
- RAM。
- データベースサービス。
- PHPワーカー・プール。
- ストレージ。
- cron・バックグラウンドジョブの実行時間帯。
- バックアップの実行時間。
- 障害の影響範囲。

アクセスが少ないキャッシュ中心の10サイトより、動的処理が多い会員サイト1つのほうが重い場合もあります。

必要に応じてユーザーとDB認証情報を分け、ドメイン数ではなく**合計のピーク負荷**からスペックを選びます。

[複数サイト向けVPS]({{< relref "vps-for-multiple-websites.md" >}})をご覧ください。

## WordPress向けVPSを増強する判断材料 {#wordpress-vps-upgrade-triggers}

実際の制約を測定してから増強します。

有力な判断材料は次のとおりです。

- メモリ不足、スワップ、OOMが継続して発生する。
- PHPワーカーの待ち行列や上限到達が繰り返される。
- キャッシュ・クエリ・プラグインを最適化しても、CPUの飽和が続く。
- 実際に必要なワーキングセットをメモリに保持できず、DBに遅延が生じる。
- ストレージの増加で安全な運用余裕を確保できなくなる。
- バックグラウンドジョブと利用者の処理が繰り返し競合する。
- 複数の稼働サイトが共有リソースを使い切る。

これらの指標が正常なのにサイトが遅い場合、VPSの増強では解決しない可能性があります。

## WordPress向けVPSの公開前チェックリスト {#wordpress-vps-launch-checklist}

| 確認項目 | 合格の条件 |
|---|---|
| WordPressの実行環境 | サポート対象のPHP・DBバージョンとHTTPS |
| PHP | FPM・実行環境が設定済みで、ワーカー数がRAMに収まる |
| データベース | 専用の認証情報を使用し、スロークエリとワーキングセットのリスクを把握 |
| キャッシュ | ページ・オブジェクト・OPcacheの各層を意図して選定 |
| cron | WP-CronまたはOSの定期実行が動作し、監視されている |
| ファイル | 所有者が正しく、`777`にせずアップロード先へ書き込める |
| HTTPS | 信頼された証明書と更新手段がある |
| バックアップ | ファイルとDBを含み、サーバー外のコピーと復元手順がある |
| 更新 | OS・WordPress・プラグイン・テーマの担当者がいる |
| 監視 | 外部からの死活監視と、CPU・RAM・ディスク・ログを確認できる |
| 再起動 | Web・PHP・DB・cronが自動で復帰する |
| 処理能力 | 本番を代表するキャッシュされない動的処理で測定済み |

稼働中のサイトを移す場合は、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})で切り替え、最終書き込み、DNS、切り戻しを確認してください。

## 現在のWordPress向けVPS構成例 {#current-wordpress-vps-examples}

以下のVDSina Standard構成は現在の選択肢の例であり、WordPressで処理できるアクセス数を保証するものではありません。

| VPS | 検討を始める際に適した用途 | 再検討が必要になる場面 |
|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/日 | 検証・テスト、またはごく軽量なキャッシュ中心のWordPress | 本番DB、複数のPHPワーカー、パネル・メールを同居させる |
| 1 vCPU / 2 GB / 40 GB — $0.50/日 | 軽量な小規模WordPress | 重いプラグイン、複数の稼働サイト、継続的な動的処理 |
| 2 vCPU / 4 GB / 80 GB — $0.67/日 | 企業のWordPressサイトの実用的な開始構成 | 重い会員制サイト・WooCommerce、大きなDB、重複するジョブ |
| 4 vCPU / 8 GB / 160 GB — $1.34/日 | 動的処理が多いWordPress・大きめのDB・複数サイト | 個別の拡張や、より強い分離が必要になる |

VDSinaの現在のStandardページでは、表示されているテンプレート・アプリの一覧に、WordPress専用のプリインストール済みアプリはありません。ワンクリックのWordPressイメージがあると決めつけず、OSから手動で構築するか、現在対応している管理パネルを利用してください。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のWordPress向けVPSを確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で申し込むと当サイトが報酬を受け取る場合があります。契約前に最新のVPS料金、テンプレート、管理パネルの提供状況を確認してください。</small></p>

## 技術資料 {#technical-references}

- WordPress.org：現在の動作要件
- WordPress開発者ハンドブック：キャッシュ
- WordPress開発者資料：オブジェクトキャッシュ
- WordPress開発者資料：OSのスケジューラーとWP-Cron
- VDSina Standard VPS

## よくある質問 {#faq}

### WordPressをVPSで動かすにはRAMがどれくらい必要ですか？ {#how-much-ram-does-wordpress-need-on-a-vps}

WordPress本体は、本番VPSに必要なRAM容量を定めていません。Linux、Webサーバー、PHPワーカー、DB、キャッシュ、パネル・メール・バックグラウンドジョブ、余裕分を含めます。軽量なサイトなら2 GBで収まる場合がありますが、企業サイトでは4 GBのほうが余裕のある実用的な開始構成です。

### WordPress向けVPSに1 GB RAMで十分ですか？ {#is-1-gb-ram-enough-for-wordpress-vps}

ごく軽量な構成やテスト用のWordPressなら動作しますが、DB、PHPワーカー、バックグラウンド処理の余裕は小さくなります。通常の本番運用の推奨構成とは考えないでください。

### WordPressに2 GB RAMで十分ですか？ {#is-2-gb-ram-enough-for-wordpress}

ソフトウェア構成が軽く、キャッシュが十分に効く小規模サイトなら足りる場合があります。PHPワーカーのメモリ、DBのRAM、プラグイン、バックグラウンドジョブを監視してください。

### WordPressに4 GB RAMで十分ですか？ {#is-4-gb-ram-enough-for-wordpress}

多くの企業のWordPressサイトでは、4 GBが実用的な検討の出発点です。重いプラグイン、会員のアクセス、WooCommerce、大きなDB、インポート、複数の稼働サイトでは、より多く必要になる場合があります。

### WordPress向けVPSは何人の訪問者に対応できますか？ {#how-many-visitors-can-a-wordpress-vps-handle}

一律に信頼できる訪問者数はありません。キャッシュヒット率、キャッシュされない同時処理数、PHPの処理時間、プラグインの負荷、DB処理、バックグラウンドジョブによって処理能力が変わります。

### VPS上のWordPressにRedisは必要ですか？ {#do-i-need-redis-for-wordpress-on-vps}

必須ではありません。オブジェクトやDBの結果を繰り返し再利用できる処理では、Redisの永続オブジェクトキャッシュが役立つ場合があります。ただし、すべてのWordPressサイトに必要なわけではなく、ページ全体のキャッシュにも代わりません。

### WordPress向けVPSではNginxとApacheのどちらを使うべきですか？ {#should-i-use-nginx-or-apache-for-wordpress-vps}

どちらも選択肢になります。WordPress.orgはApacheとNginxを堅実な選択肢として推奨しています。アプリの要件に合い、管理者が安定して運用できる構成を選んでください。

### WP-CronをOSのcronに置き換えるべきですか？ {#should-i-replace-wp-cron-with-system-cron}

決まった間隔の実行が処理内容に適しており、代わりの起動設定を正常に動かせる場合に検討します。別の起動手段なしにWP-Cronを無効化しないでください。

### WordPress向けVPSに管理パネルは必要ですか？ {#does-wordpress-vps-need-a-control-panel}

必須ではありません。手動管理のLinux VPSでもWordPressを運用できます。パネルは任意の選択肢であり、性能の要件ではなく管理のしやすさで選んでください。

### VDSinaにはWordPressがプリインストールされていますか？ {#does-vdsina-include-wordpress-preinstalled}

現在のStandard VPSページでは、表示されているテンプレート・アプリの一覧に、WordPress専用のプリインストール済みアプリはありません。テンプレートが利用できるかは、実際の申込画面で確認してください。
