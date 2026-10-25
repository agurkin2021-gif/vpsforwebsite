---
title: "VPSの監視"
description: "VPSを外部の稼働確認、CPU・RAM・ディスク・ネットワーク指標、サービスの状態、ログ、対応につながる通知で監視。ツール、しきい値、実践的なチェックリストを解説します。"
image: "images/home/vps-for-website-hero.webp"
slug: "vpsの監視"
---

VPSの監視では、サーバーが起動しているか以上のことを確認します。本番環境の基本構成には、**外部の稼働確認、ホスト指標の履歴、サービス・アプリケーションの正常性、ログ、対応につながる通知、明確な対応担当者**が必要です。

pingに応答していても、Nginxが壊れ、DBが停止し、ディスクが満杯になり、TLS証明書が期限切れ間近という場合があります。サーバーと、利用者がアクセスするサイトの両方を監視してください。

サーバー選び全体の考え方は、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[要点](#quick-answer) · [チェックツール](#vps-monitoring-baseline-checker) · [ホスト指標](#monitor-cpu-memory-disk-and-network) · [アプリの状態](#monitor-services-and-application-health) · [通知](#build-actionable-alerts) · [容量計画](#use-trends-for-capacity-planning) · [よくある質問](#faq)

## 構成の目安 {#quick-answer}

実用的なVPS監視は、5つの層で考えます。

| 層 | 分かること | 検知できる代表的な障害 |
|---|---|---|
| **外部からの稼働確認** | VPS外から利用者がサイトへ到達できるか | VPS・ネットワーク・サイトへの接続不能 |
| **ホスト指標** | CPU、RAM、スワップ、ディスク、inode、I/O、ネットワークの推移 | メモリリーク、容量不足、継続するCPU逼迫 |
| **サービス・アプリの正常性** | Webサーバー、実行環境、DB、重要なエンドポイントが実際に動くか | サーバーは稼働中でもNginx・PHP・DB・アプリが故障 |
| **ログ・イベント** | 何が変わり、何が失敗したか | 5xx急増、OOM、ワーカー停止、DBエラー |
| **通知と担当者** | 適切な人に届き、対応できるか | 気づかない停止、見られないダッシュボード |

監視対象と同じVPSに唯一の稼働監視を置かないでください。VPSやネットワークが完全に停止すると、監視も一緒に失われます。

## VPS監視の基本構成チェック {#vps-monitoring-baseline-checker}

監視の死角を見つけるツールです。稼働率を保証するものではありません。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">主な処理内容</label>
    <select id="mon-workload" class="form-input">
      <option value="static">静的・単純なWebサイト</option>
      <option value="cms">WordPress・CMS</option>
      <option value="transactional">WooCommerce・取引サイト</option>
      <option value="multi">複数サイト・異なる用途の混在</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">このVPSの外からHTTP(S)の稼働を確認している？</label>
    <select id="mon-external" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">CPU・RAM・ディスク・ネットワークの履歴を保持している？</label>
    <select id="mon-metrics" class="form-input"><option value="no">いいえ・必要時のtop/htopだけ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">ディスク容量、inode、ストレージの逼迫を監視している？</label>
    <select id="mon-disk" class="form-input"><option value="no">いいえ・空きGBだけ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">重要なサービス・アプリの正常性確認を設定済み？</label>
    <select id="mon-app" class="form-input"><option value="no">いいえ・pingだけ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">必要なDB・キュー・cron・バックアップの鮮度を監視している？</label>
    <select id="mon-jobs" class="form-input"><option value="no">いいえ・不明</option><option value="yes">はい</option><option value="na">対象外</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">重要度と継続時間のルールを使う自動通知がある？</label>
    <select id="mon-alerts" class="form-input"><option value="no">いいえ・ダッシュボードだけ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">このVPSが停止しても通知経路は使える？</label>
    <select id="mon-notify" class="form-input"><option value="no">いいえ・同じVPSだけ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">担当者と初動対応の手順書がある？</label>
    <select id="mon-owner" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <button class="btn btn-primary" type="submit">監視の基本構成を確認</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">実際にデータを収集し、通知が届く監視だけを「はい」にしてください。</p>
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
      result = "監視の死角あり：基本的な障害の一部をまだ検知できません。独立した稼働確認、ホスト指標の履歴、ディスク・inodeの可視化、実際のサービス・アプリケーションの正常性確認を追加してください。";
    } else if (!alerts || !notify || !owner) {
      result = "通知・担当体制が未整備：データがあっても、障害を見逃したり、対応者がいなかったりする可能性があります。対応につながる通知、独立した通知経路、担当者を明記した初動手順を用意してください。";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "基本的な監視あり：インフラ監視はありますが、この用途で必要なアプリケーションの定期処理、DB、バックアップの鮮度がまだ監視できていません。";
    } else {
      result = "本番監視の基本構成あり：外部の稼働確認、指標の履歴、サービスの状態、通知、対応担当者がそろっています。実際の通常値に合わせてしきい値を調整し続けてください。稼働率を保証するものではありません。";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## VPSの外からWebサイトを監視する {#monitor-the-website-from-outside-the-vps}

内部コマンドではNginxの稼働を確認できますが、インターネット上の利用者がサイトへ到達できる証明にはなりません。

重要なホスト名には外部監視を使います。

次のチェックが役立ちます。

- HTTP/HTTPSの利用可能性。
- 期待するステータスコード。
- 応答時間。
- キーワード・内容の確認。
- DNS名前解決。
- TLS証明書の状態・有効期限。
- 必要に応じたTCPポートの確認。

誤通知を抑えたい場合は、失敗の繰り返しや複数地点での確認を条件にしてから、担当者を呼び出します。

Uptime Kumaなどの自己ホスト型ツールでは、HTTP(S)、キーワード、TCP、ping、DNSを確認できます。ただし、本番VPSと障害範囲を共有しない場所に置いてください。

同じVPS、事業者ネットワーク、DNSの障害を共有する監視サーバーは、ダッシュボードには役立っても、独立した稼働確認にはなりません。

## リアルタイムの診断と履歴を残す監視は別 {#real-time-diagnostics-are-not-historical-monitoring}

次のようなコマンドは、

```bash
top
htop
free -h
df -h
ss -s
```

すでに問題を調査している際に役立ちます。

ただし、次は分かりません。

- 03:12に何が起きたか。
- RAMが6時間にわたって増え続けたか。
- バックアップ中にディスク遅延が急増したか。
- サイトが10分間停止していたか。
- 問題が週ごとに悪化しているか。

稼働と容量に影響する指標は、時系列の履歴を保持します。

1台のVPSなら軽量な監視エージェントで足りる場合があります。複数台、長期保存、独自ダッシュボードには、Prometheus + Node Exporter + Grafanaが一般的な構成です。

Prometheus Node Exporterは、CPU、ファイルシステム、ネットワークなど、Prometheusが収集できるホスト・カーネル指標を公開します。

## CPU・メモリ・ディスク・ネットワークを監視する {#monitor-cpu-memory-disk-and-network}

### CPU {#cpu}

短い急増のたびに通知しないでください。

次を確認します。

- 継続するCPU使用率。
- vCPU数に対するロードアベレージ。
- プロセスごとのCPU使用量。
- 仮想化環境で取得できる場合はCPU steal時間。
- 同じ時間帯のアプリケーション・リクエスト遅延。

キャッシュのウォームアップやcronで一時的に100%になっても、問題がない場合があります。CPU飽和が続き、遅延やキューも増えるなら、実際のボトルネックを示す根拠が強くなります。

### メモリ・スワップ・OOM {#memory-swap-and-oom}

Linuxは余ったRAMをファイルシステムのキャッシュに使うため、「RAM使用率90%」だけで障害とは判断できません。

次を確認します。

- 利用可能なメモリ。
- スワップの入出力。
- スワップ使用量の増加。
- OOM killerの発生。
- プロセスのメモリ増加。
- PHP・アプリケーションワーカーのメモリ。
- データベースのメモリ。

メモリリークは昼には正常に見えても、夜間にプロセスを停止させる場合があります。履歴の傾向が発見に役立ちます。

### ディスク容量 {#disk-capacity}

DB、ログ、パッケージ更新が失敗する前に、ファイルシステムの使用率を確認します。

警告・重大の初期目安として**使用率80% / 90%**を使う例がありますが、共通のSLAではありません。急増するDBでは、さらに早い対応が必要な場合があります。

次の作業に必要な空き容量も監視します。

- バックアップ。
- データベース保守。
- パッケージ更新。
- アップロード。
- ログ。
- ステージング・インポート処理。

### inode {#inodes}

多くのGBが空いていても、inodeが尽きる場合があります。

例えば、次で発生します。

- キャッシュディレクトリー。
- セッション。
- メールキュー。
- 大量の小さなファイル。
- 一時ファイルの異常増加。

inode使用量は、ディスクのGBとは別に追跡します。

### ディスクI/Oと遅延 {#disk-io-and-latency}

容量が満杯になる前に、ディスクがボトルネックになる場合があります。

次を確認します。

- I/O待ち。
- 読み取り・書き込み遅延。
- 取得できる場合はキューの深さ。
- データベースの応答時間。
- バックアップ・インポートの時間帯。

ディスク容量を増やしても、遅いストレージI/Oが自動的に改善するわけではありません。

### ネットワーク {#network}

総帯域だけでなく、次も追跡します。

- 受信・送信のスループット。
- トラフィックの急変。
- 接続エラー。
- 測定できる場合はパケット損失・遅延。
- 異常な外向き通信。
- インターフェースのエラー。

ネットワーク指標は、アプリケーションの遅さと事業者・経路の問題を切り分けるのに役立ちます。

## サービスとアプリケーションの正常性を監視する {#monitor-services-and-application-health}

VPSに到達できても、サイトが壊れている場合があります。

次のような重要サービスを監視します。

- Nginx・Apache。
- PHP-FPM。
- Node・Pythonのアプリケーションサービス。
- MySQL・MariaDB・PostgreSQL。
- 使用する場合はRedis。
- キューワーカー。
- 定期処理のサービス。
- 業務上重要な場合はコントロールパネル。

systemdを使うLinuxでは、診断時に`systemctl --failed`が役立ちます。ただし継続監視では、必須サービスの失敗や再起動の繰り返しを通知する必要があります。

プロセスが存在することだけで確認を終えないでください。動いていても、正しいリクエストを処理できない場合があります。

## HTTP 200でも正常とは限らない {#http-200-is-not-always-healthy}

アプリケーションがHTTP 200で次を返す場合があります。

- メンテナンスページ。
- テンプレート内に表示されたDBエラー。
- 空の内容・誤った内容。
- 壊れたログイン処理。
- 古いキャッシュ。

重要なサイトでは、目的に合う最小限の確認を選びます。

- 期待するキーワード・テキスト。
- ヘルスチェック用エンドポイント。
- API応答。
- 重要な公開URL。
- 複雑さに見合う業務上の価値がある場合に限り、ログイン・取引の合成テスト。

安全に変更するよう特別に設計していない限り、合成テストで本番データを変更しないでください。

## TLSとDNSを監視する {#monitor-tls-and-dns}

VPSが正常でも、証明書やDNSの問題でサイトが利用できなくなる場合があります。

次を追跡します。

- 証明書の有効期限。
- 証明書とホスト名の不一致。
- 更新の失敗。
- DNS名前解決。
- ツールが対応する場合は、意図しないレコード変更。

例えば、期限の**14日前**に警告し、**7日前**に近づいたら対応を引き上げる方法があります。具体的な期間は、更新問題をどれだけ早く直せるかに合わせます。

## アプリケーションの依存先としてDBを監視する {#monitor-the-database-as-an-application-dependency}

DBを使うサイトでは、DBがボトルネックや故障した依存先になっているか判断できるだけの情報を集めます。

エンジンと処理内容によって、次の指標が役立ちます。

- サービスの利用可能性。
- 接続数。
- 接続エラー。
- クエリの遅延。
- ロック・競合の兆候。
- 遅いクエリの発生状況。
- メモリ不足。
- ストレージの増加。
- 使用している場合は、レプリケーション・バックアップの状態。

すべてのDB指標で通知せず、利用者への影響や既知の障害パターンに結び付く条件を通知します。

WordPressの負荷特性は、[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})をご覧ください。取引ストアの負荷は、[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})で説明しています。

## cron・キュー・バックグラウンド処理を監視する {#monitor-cron-queues-and-background-jobs}

ホームページが正常でも、バックグラウンド処理が正常とは限りません。

アプリケーションに重要な処理を追跡します。

- cron。
- キューワーカー。
- 定期インポート。
- Webhook。
- メール送信処理。
- WordPressのWP-Cron・システムcron。
- WooCommerce Action Scheduler。
- 定期購入・更新。
- 在庫同期。

役立つ指標は次のとおりです。

- 最後に成功した実行。
- キューの長さ・滞留量。
- 失敗したジョブ。
- 最も古い未処理ジョブ。
- 再試行の繰り返し。
- ワーカーの停止・再起動。

WooCommerceでは、商品一覧が表示できても、Action Schedulerの失敗・期限超過キューが増えると運用上の問題になります。

## バックアップの鮮度を監視する {#monitor-backup-freshness}

バックアップジョブは復旧戦略の一部ですが、**最後に成功したバックアップの古さは監視対象**です。

次の場合に通知します。

- 定期バックアップが失敗した。
- 最新の成功バックアップが、定めたRPOより古い。
- DBダンプが失敗した。
- 外部へのアップロードが失敗した。
- リポジトリーの認証情報が期限切れになった。
- バックアップサイズが不自然に変化した。
- 古いデータの削除・保持処理が失敗した。

cronが動いたことを、利用可能なバックアップがある証拠にしないでください。

RPO/RTO、保持期間、独立コピー、復元訓練は、[VPSのバックアップ戦略]({{< relref "vps-backup-strategy.md" >}})をご覧ください。

## ログと指標を同じ時間帯で照合する {#correlate-logs-with-metrics}

指標は**何が変わったか**を示し、ログは多くの場合**なぜ変わったか**を示します。

同じ時間帯について、次を照合します。

- Nginx/Apacheのアクセス・エラーログ。
- PHP-FPM・実行環境のログ。
- アプリケーションログ。
- データベースログ。
- システムジャーナル。
- 認証ログ。
- バックアップ・定期処理のログ。

例：

- 14:03にCPUが急増する。
- 14:03に5xxが増える。
- アプリケーションログにDBタイムアウトがある。
- DBログにロック競合がある。

単なる「CPU使用率が高い」という通知より、具体的な対応につながります。

調査に十分な期間ログを保持しつつ、本番のファイルシステムをログで満杯にしないでください。

## 対応につながる通知を作る {#build-actionable-alerts}

通知には、何が失敗し、最初に何を調べるかを示します。

次を優先します。

- **警告** — 利用者への影響が出る前に調査。
- **重大** — 利用者への影響、または差し迫った障害。
- 継続時間・瞬間変動の抑制 — 1秒の急増で呼び出さない。
- 集約・重複排除 — 1件の障害で40件の通知を送らない。
- 影響を受けるホスト・サービスを明示。
- ダッシュボード・ログ・手順書へのリンク。
- 決められた初動・エスカレーション。

Prometheus Alertmanagerは、通知の集約、重複排除、振り分けを行う仕組みの例です。

### すべてに同じしきい値を使わない {#avoid-universal-thresholds}

しきい値は処理内容に合わせます。

最初の判断ルールの例は次のとおりです。

- CPU：単発の急増ではなく、高負荷の継続と遅延・キューの兆候。
- RAM：「使用率 > 80%」だけではなく、利用可能メモリの減少とスワップ・OOM。
- ディスク：運用上の余裕が残っている段階で早めに警告。
- TLS：期限切れの数日前から警告。
- HTTP：誤検知が問題になる場合は、失敗の繰り返しや複数地点での確認。
- バックアップ：最後の成功がRPOより古い。
- 5xx・遅延：通常の基準からの継続的な逸脱。

本番の通常時の動作を観察してから調整します。

## 通知経路を独立させる {#keep-the-notification-path-independent}

同じ障害で配信システムも止まれば、通知は役に立ちません。

可能な範囲で、重要な通知はVPS外の経路で送ります。

- 外部メール事業者。
- 外部のチャット・通知サービス。
- ホスト型のインシデント管理ツール。
- 別の障害範囲にある監視環境。

故障したVPS上のSMTPサーバーやダッシュボードだけに頼らないでください。

## すべての通知に担当者と手順書を用意する {#every-alert-needs-an-owner-and-runbook}

通知を作る前に、次を決めます。

- 誰が受け取るか。
- 誰に対応権限があるか。
- 最初の診断手順は何か。
- どのダッシュボード・ログを開くか。
- いつエスカレーションするか。
- いつ安全に通知を抑制できるか。
- 営業時間外はどう対応するか。

対応者がいなければ、監視は停止を通知に変えただけです。

運用全体の責任分担は、[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})をご覧ください。

## 複雑さに合わせて監視構成を選ぶ {#choose-the-monitoring-stack-by-complexity}

人気があるという理由だけで、大規模な可観測性基盤を導入しないでください。

### 事業者のダッシュボードを出発点にする {#provider-dashboard-as-a-starting-layer}

事業者がCPU、RAM、ディスク、ネットワークの履歴を提供していれば、ホスト監視の便利な出発点として使います。

ただし、事業者側のインフラグラフは、Webサイト全体の監視ではありません。事業者外からのHTTP(S)経路、アプリの内容、DB、定期処理、TLS更新、通知の担当までは確認しない場合があります。

事業者の監視を情報源の1つとして使い、用途に必要な外部・アプリケーション側の確認を追加します。

### 1台のVPS向けの軽量な構成 {#lightweight-single-vps-path}

小規模環境では、次を組み合わせられます。

- 外部の稼働監視。
- Netdataなどのホスト指標エージェント・ダッシュボード。
- システム・アプリケーションのログ。
- 通知。

1人の担当者が1台または少数のVPSを管理する場合に適しています。

### Prometheus・Grafanaを使う構成 {#prometheus--grafana-path}

次が必要な場合に役立ちます。

- 複数サーバーの指標。
- 長期間の履歴保持。
- 独自のクエリ。
- サービス・Exporterの指標。
- 共有ダッシュボード。
- 体系的な通知ルール。

Node ExporterがLinuxホスト指標を提供し、Prometheusが保存・検索し、Grafanaが可視化します。Alertmanagerでは通知の振り分け、集約、重複排除ができます。

### ホスト型監視サービスを使う構成 {#hosted-monitoring-path}

次の場合に役立ちます。

- 監視を自分のVPS・事業者から独立させる必要がある。
- 自分で運用する監視インフラを減らしたい。
- 管理された通知・オンコール連携に価値がある。

監視システム自体も本番インフラです。減らせるリスクに見合う複雑さに抑えてください。

## 監視基盤を保護する {#secure-the-monitoring-stack}

監視エージェントやダッシュボードから、機密性のある運用情報が見える場合があります。

次を保護します。

- ダッシュボード。
- Exporter。
- 指標のエンドポイント。
- APIトークン。
- 通知用Webhook。
- ログの保存・検索基盤。

明確で安全なアクセス方式を用意せず、Prometheus、Node Exporter、Grafana、管理ダッシュボードをインターネット全体へ公開しないでください。

必要に応じて、ファイアウォール、プライベートネットワーク、リバースプロキシの認証を使います。

監視は保護強化の代わりにはなりません。基本の対策は、[VPSのセキュリティチェックリスト]({{< relref "vps-security-checklist.md" >}})をご覧ください。

## 監視自体のリソース消費も考慮する {#monitoring-overhead-matters}

監視は次を消費します。

- RAM。
- CPU。
- 指標・ログの保持用ディスク。
- ネットワーク。
- バックアップ容量。

小さなエージェントは通常軽量ですが、長期間の指標・ログ保存は大きなストレージ負荷になり得ます。

監視基盤自体も確認します。

- エージェント・サービスの状態。
- 指標収集の失敗。
- ストレージの増加。
- 保持期間。
- 通知の配信。

ディスクを守るための監視で、そのディスクを満杯にしないでください。

## 推移を容量計画に生かす {#use-trends-for-capacity-planning}

監視履歴は、次のスペック選びの有力な根拠になります。

推移から次を判断します。

- CPU飽和は継続的か、一時的か。
- 利用可能RAMが数週間にわたり減っているか。
- 正常な利用負荷でスワップ・OOMが発生しているか。
- ディスクはどの速さで増えているか。
- アクセスピーク時にDB遅延が増えるか。
- PHP・アプリのキューができるか。
- バックアップ・インポートが予測可能な競合を生んでいるか。

ダッシュボードが一瞬赤くなっただけで増強しないでください。

**最適化済みの正常な処理負荷**が繰り返しリソースを使い切る場合や、構成上個別の拡張が必要な場合に増強・分離します。

監視結果をリソースの判断へつなげるには、[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})をご覧ください。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のVPS構成を確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で注文されると当サイトが報酬を受け取る場合があります。スペックは監視データに基づいて選んでください。このページは、VDSinaが上記の監視ツールを管理サービスとして提供すると説明するものではありません。</small></p>

## 複数サイトは2つの階層で監視する {#monitor-multiple-websites-at-two-levels}

複数サイトのVPSでは、次を監視します。

### サーバー全体 {#server-level}

- CPU・RAM・スワップ。
- ディスク・inode・I/O。
- データベース。
- ネットワーク。
- 主要サービス。

### サイト単位 {#site-level}

- 重要な各ホスト名。
- TLS。
- 応答時間。
- 5xx。
- アプリ・定期処理の失敗。
- 取得できる場合は、サイト別ログとワーカーの逼迫。

サーバーが正常でも、1つの仮想ホスト、証明書、サイトが壊れている場合があります。

集約と障害範囲の判断は、[複数サイト向けVPS]({{< relref "vps-for-multiple-websites.md" >}})をご覧ください。

## VPS監視のチェックリスト {#vps-monitoring-checklist}

| 指標・機能 | 合格条件 |
|---|---|
| 外部稼働確認 | 重要なホスト名をVPS外から確認している |
| HTTP正常性 | 期待するステータス・内容・ヘルスエンドポイントを検証している |
| CPU | 継続的な使用率・負荷・プロセス別の履歴を保持している |
| RAM | 利用可能メモリ、スワップ、OOMを把握できる |
| ディスク | 容量と増加量を監視している |
| inode | inode枯渇を別に監視している |
| I/O | ストレージが重要な場合、遅延・I/O待ちを把握できる |
| ネットワーク | スループット・エラー・経路の問題を観測できる |
| サービス | Web・実行環境・DB・ワーカーを監視している |
| データベース | アプリに関係する稼働状況・遅延・接続数が見える |
| 定期処理 | cron・キュー・バックグラウンドの失敗や滞留が見える |
| TLS・DNS | 期限切れと名前解決の失敗を検知できる |
| バックアップ | 最後の成功からの時間とジョブ失敗を監視している |
| ログ | Web・アプリ・DB・システムのログを同時刻で照合できる |
| 通知 | 警告・重大と、継続時間・瞬間変動の抑制を設定した |
| 通知経路 | 重要な通知がVPSの障害範囲外を通る |
| 担当体制 | 対応者と初動手順書がある |
| 保持期間 | 傾向と根本原因を調べるのに十分な履歴がある |
| セキュリティ | 監視エンドポイント・画面を意図せず公開していない |
| 容量計画 | 推移を最適化・拡張の次の判断に使っている |

## 技術資料 {#technical-references}

- Prometheus — Node ExporterによるLinuxホスト指標の監視
- Prometheus — Alertmanager
- Uptime Kuma — 公式プロジェクト
- [VPSのバックアップ戦略]({{< relref "vps-backup-strategy.md" >}})
- [VPSのセキュリティチェックリスト]({{< relref "vps-security-checklist.md" >}})

## よくある質問 {#faq}

### VPSでは何を監視すべきですか？ {#what-should-i-monitor-on-a-vps}

少なくとも、外部からのサイト利用、CPU、利用可能RAM・スワップ・OOM、ディスク容量、inode、主要サービス、アプリの正常性、TLS期限、バックアップの鮮度、通知配信を監視します。

### CPU使用率80%超は必ず問題ですか？ {#is-cpu-over-80-always-bad}

いいえ。短い高負荷は正常な場合があります。継続的な使用率と、負荷、リクエスト遅延、キュー、処理しているプロセスを合わせて調査してください。

### LinuxのRAMがほぼ満杯なのはなぜですか？ {#why-is-linux-ram-almost-full}

Linuxは空きメモリをキャッシュに使います。使用率だけで警告せず、利用可能メモリ、スワップの動き、OOM、プロセスの増加を確認してください。

### ディスクの問題には何を監視すべきですか？ {#what-should-i-monitor-for-disk-problems}

ファイルシステム容量、inode使用量、ストレージの増加、I/O遅延・待ちを監視します。空きGBだけではすべての障害を捉えられません。

### 稼働監視はpingだけで十分ですか？ {#is-ping-enough-for-uptime-monitoring}

いいえ。サイト、DB、TLSに問題があってもpingは成功する場合があります。利用者から見た正常性には、HTTP(S)とアプリ・サービスの確認を使ってください。

### 稼働監視を同じVPSで動かしてよいですか？ {#should-the-uptime-monitor-run-on-the-same-vps}

唯一の監視としては不十分です。VPSやネットワークの完全停止で、サイトと一緒に監視も止まります。少なくとも重要な稼働確認と通知経路は、その障害範囲の外に置いてください。

### VPS監視にはどのツールが最適ですか？ {#which-vps-monitoring-tool-is-best}

万能なツールはありません。1台なら外部稼働監視と軽量なホスト指標エージェントで足りる場合があります。複数台ではPrometheus、Grafana、Alertmanagerが適する場合があります。必要な可視性、保持期間、運用の複雑さで選びます。

### 1台のVPSでもPrometheusとGrafanaは必要ですか？ {#do-i-need-prometheus-and-grafana-for-one-vps}

必須ではありません。長期の指標、独自クエリ、複数サーバーには強力ですが、小規模環境では軽量エージェントと外部稼働監視で十分な場合があります。

### バックアップはどう監視すべきですか？ {#how-should-i-monitor-backups}

ジョブ失敗と、RPOに対して最新の成功バックアップがどれだけ古いかを通知します。復旧可能性は、別途復元テストで確認してください。

### どの監視結果でVPSを増強すべきですか？ {#when-should-monitoring-trigger-a-vps-upgrade}

最適化済みの正常な処理負荷が、CPU、RAM、ストレージ・I/Oなどを繰り返し使い切っていると履歴で分かる場合です。単発の急増だけでは十分な根拠になりません。
