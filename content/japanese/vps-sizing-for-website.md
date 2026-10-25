---
title: "VPSのスペックの選び方"
description: "VPSのCPU・RAM・ストレージを実際の負荷から計算。共用サーバーの制限、PHPワーカー、データベース、ピーク時の処理を基に、サイトに合うスペックを選びます。"
image: "images/home/vps-for-website-hero.webp"
slug: "vpsのスペックの選び方"
---

VPSのスペック選定は、月間訪問者数ではなく、オリジンサーバーに届く処理負荷から始めます。キャッシュできる割合、動的リクエストの同時実行、PHP・アプリワーカー、DB処理、バックグラウンドジョブ、管理パネルの消費量、ストレージの増加によって、サイトに必要なCPU・RAM・ディスクが決まります。

契約判断全体の考え方は、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[RAMの見積もり](#ram-budget) · [共用サーバーの診断](#shared-hosting-to-vps-diagnostic) · [結果に合うプラン](#match-the-result-to-a-vps) · [よくある質問](#faq)

## スペック選定の目安 {#quick-sizing-answer}

以下のVDSina Standard構成は、比較の基準として使えます。プランに負荷を合わせるのではなく、負荷に合うプランを選んでください。事業者の数値の確認日は2026年10月13日です。

| サイトの用途・負荷 | 開始構成の例 | 確認すること |
|---|---:|---|
| ごく軽量なサイト、検証環境、キャッシュを十分に活用するサイト | 1 vCPU / 1 GB RAM / 10 GB — $0.07/日、転送量1 TB/月 | メモリの余裕、DBサイズ、スワップの使用 |
| 小規模サイト・軽量なCMS | 1 vCPU / 2 GB RAM / 40 GB — $0.50/日、転送量32 TB/月 | PHPワーカー、管理パネルの消費量、DBメモリ |
| 企業サイト・一般的な動的処理のあるWordPress | 2 vCPU / 4 GB RAM / 80 GB — $0.67/日、転送量32 TB/月 | キャッシュされない同時処理、cronジョブ、DB遅延 |
| 動的処理が多いサイト、大きめのDB、複数の稼働サイト | 4 vCPU / 8 GB RAM / 160 GB — $1.34/日、転送量32 TB/月 | 継続的なCPU負荷、ワーカーのメモリ、ピークの重なり |

これは選定の方向性であり、アクセス数の保証ではありません。同じ訪問者数でも、必要なサーバーは大きく異なります。料金、転送量、その他の条件は変更される場合があるため、契約前に最新の提供内容を確認してください。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のVPS構成を確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で申し込むと当サイトが報酬を受け取る場合があります。推奨スペックは報酬ではなく処理負荷を基に選定しています。</small></p>

## 選定の考え方：アクセス数より先にリソースを見積もる {#the-sizing-model-reserve-resources-before-counting-traffic}

VPSの見積もりでは、サーバーをリソースの消費元ごとに分けて考えます。

### RAMの見積もり {#ram-budget}

RAM全体には、次の用途を含めます。

1. OSとシステムサービス。
2. Webサーバー・リバースプロキシ。
3. PHP-FPM、Node.js、Pythonなどのアプリ実行環境。
4. データベース。
5. 使用する場合はRedisなどのキャッシュサービス。
6. 管理パネルと付属サービス。
7. 監視、セキュリティ、バックアップのプロセス。
8. 同時に動くアプリケーションワーカー。
9. 急増、デプロイ、保守に備える安全な余裕。

CMSのメモリ上限をサーバー全体のRAM要件と捉えないでください。PHPのメモリ上限が256 MBだからといって、1 GB VPSで256 MBのPHPプロセス4個に加え、Linux、DB、その他すべてのサービスを安全に動かせるわけではありません。

実用的には、次のように考えます。

**必要なRAM＝基本サービス＋DBの使用メモリ＋同時実行ワーカーのメモリ＋バックグラウンドジョブのメモリ＋余裕**

可能な限り、実際のプロセスを測定してください。見積もりは開始プランを選ぶのに役立ちますが、本当に足りるかは実測で判断します。

### RAM見積もりツール {#ram-budget-estimator}

訪問者数から推測せず、このツールで前提条件を明らかにできます。見積もるのはRAMのみで、CPU、ストレージ、I/Oは別に検証が必要です。自分の測定値を入力してください。入力欄の例は下記の計算例に対応し、すべてのサイトに使える標準値ではありません。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="ram-budget-estimator-form">
  <div class="mb-6">
    <label for="ram-baseline" class="form-label">OSと基本Webサービスのメモリ（MB）</label>
    <input id="ram-baseline" class="form-input" type="number" min="0" step="1" placeholder="450" required>
  </div>
  <div class="mb-6">
    <label for="ram-database" class="form-label">DBの使用メモリ（MB）</label>
    <input id="ram-database" class="form-input" type="number" min="0" step="1" placeholder="500" required>
  </div>
  <div class="mb-6">
    <label for="ram-workers" class="form-label">同時稼働するアプリワーカー数</label>
    <input id="ram-workers" class="form-input" type="number" min="0" step="1" placeholder="6" required>
  </div>
  <div class="mb-6">
    <label for="ram-worker-mb" class="form-label">ワーカーあたりの平均メモリ（MB）</label>
    <input id="ram-worker-mb" class="form-input" type="number" min="0" step="1" placeholder="120" required>
  </div>
  <div class="mb-6">
    <label for="ram-background" class="form-label">パネル・キャッシュ・バックグラウンドジョブ（MB）</label>
    <input id="ram-background" class="form-input" type="number" min="0" step="1" placeholder="300" required>
  </div>
  <div class="mb-6">
    <label for="ram-headroom" class="form-label">安全のための余裕（%）</label>
    <input id="ram-headroom" class="form-input" type="number" min="0" max="100" step="1" value="25" required>
  </div>
  <button class="btn btn-primary" type="submit">RAMの構成を見積もる</button>
</form>
<p id="ram-budget-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">測定値を入力して必要なメモリを計算してください。</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("ram-budget-estimator-form");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function number(id) {
      var value = Number(document.getElementById(id).value);
      return Number.isFinite(value) && value >= 0 ? value : 0;
    }
    var baseline = number("ram-baseline");
    var database = number("ram-database");
    var workers = number("ram-workers");
    var workerMb = number("ram-worker-mb");
    var background = number("ram-background");
    var headroom = number("ram-headroom");
    var subtotal = baseline + database + (workers * workerMb) + background;
    var required = subtotal * (1 + headroom / 100);
    var requiredGb = Math.round((required / 1024) * 10) / 10;
    var tier;
    if (required <= 1024) tier = "1 GB RAM";
    else if (required <= 2048) tier = "2 GB RAM";
    else if (required <= 4096) tier = "4 GB RAM";
    else if (required <= 8192) tier = "8 GB RAM";
    else tier = "8 GB RAM超、または処理を分離した構成";
    document.getElementById("ram-budget-result").textContent =
      "同時稼働に必要なメモリの概算：約" + requiredGb + " GB（余裕分を含む）。RAMだけで見た開始構成：" + tier +
      "。契約前に、実際のプロセスメモリとCPU負荷を検証してください。";
  });
});
</script>

計算例：基本サービス450 MB＋DB用500 MB＋6ワーカー×120 MB＋パネル・キャッシュ・バックグラウンドジョブ300 MB＝余裕分を加える前で1,970 MBです。25%の余裕を含めると約2.4 GBになります。この前提では2 GB VPSは窮屈で、4 GBのほうが安全な開始構成です。

PHP-FPMなどのワーカーを測定する際は、RSSの単純合計ではプロセス間で共有するメモリページやライブラリを重複計上することがある点に注意してください。測定値は判断材料であり、常に正確に足し合わせられる値ではありません。

### CPUの見積もり {#cpu-budget}

CPUの必要量は、同時に実行する処理の量によって変わります。キャッシュから静的ファイルを配信する処理は軽い場合があります。一方、アプリコードの実行、DB問い合わせ、ページ生成、画像リサイズ、インポート、API処理を行う動的リクエストは、より多くのCPUを消費します。

次の状態を確認します。

- 必要なアクセス処理の間、CPUの飽和が続く。
- CPUが使用中のときに、アプリのリクエスト処理時間が長くなる。
- 負荷の高い動的リクエストが同時に複数届く。
- cronジョブ、バックアップ、インポートが利用者のアクセスと重なる。
- 非効率なインデックスや過剰な処理により、DBクエリがCPUを消費する。

CPUの短い急上昇だけで、すぐに増強が必要とは限りません。必要な処理を遅らせる継続的な飽和のほうが、強い判断材料になります。

同時処理数は、次の式で概算できます。

**実行中の動的リクエスト数≈1秒あたりの動的リクエスト数×処理時間**

例：キャッシュされない動的リクエストが毎秒6件、p95の処理時間が0.8秒なら、その時点で約4.8件が処理中になる目安です。1リクエストに1ワーカーが必要なら、約5個の使用中ワーカーに加えて待ち行列と余裕分を見込みます。1件が0.12 CPU秒を使う場合、毎秒6件では余裕分を加える前で毎秒約0.72 CPU秒の仕事量です。これは負荷の概算であり、vCPU性能の一律の保証ではありません。CPU世代、競合、事業者のスケジューリングによって差があります。

## Webサイトの負荷の例 {#website-workload-examples}

オリジンに届く処理量は用途によって異なるため、同じアクセス数でもVPSの要件は大きく変わります。

| 用途・負荷 | 主なリソースへの影響 | スペック選定への意味 |
|---|---|---|
| 静的コンテンツ中心・キャッシュを十分に使うサイト | アプリのCPU負荷と同時ワーカー数が少なく、ファイル配信が中心 | 小さく始められるが、OS、ログ、バックアップ、予期しない非キャッシュ処理の分も確保 |
| 小規模なWordPressサイト | PHPワーカー、DB読み取り、プラグイン・cronの処理 | 月間アクセス数より、RAMとワーカーの余裕が重要になることが多い |
| WooCommerceなど取引を行うサイト | キャッシュされないカート・購入手続き・アカウントセッション、定期実行処理、DB書き込みの増加 | 動的な同時処理、DB遅延、ピークの重なりを優先。1–2 GBを本番の標準と決めつけない |
| 複数サイト | PHP・アプリワーカー、DB、cron、重複するピークの合計 | 合計のピーク負荷で選定し、一つのサイトが他のリソースを奪う場合は分離を検討 |
| バックグラウンドワーカー・自動化が多いサイト | キュー、インポート、エクスポート、API呼び出し、画像処理、定期ジョブ | 利用者への応答処理とは別にCPU・RAMを確保し、突発的なジョブがサイトを妨げる場合はワーカーを分離 |

これは負荷の傾向であり、プラットフォームの性能保証ではありません。測定値がある場合は、それを使ってください。

## 共用サーバーの制限をVPS要件に置き換える {#translate-shared-hosting-limits-into-vps-requirements}

サイトが共用サーバーで稼働中なら、スペック選定に役立つデータが、すでにホスティングの管理画面にあるかもしれません。

次の情報を集めます。

- CPU使用率と上限到達の記録。
- 物理メモリの使用量。
- エントリープロセス数・同時リクエスト数の制限。
- プロセス数。
- ディスクI/O・IOPSの負荷。
- DBサイズと増加量。
- ストレージ使用量。
- 月間アクセス数だけでなく、時間帯別のピーク。
- 確認できる場合は、PHPワーカーやアプリプロセスの動作。

### 共用サーバーからVPSへの移行診断 {#shared-hosting-to-vps-diagnostic}

障害の傾向から、プラン選定前に調べるべき点を確認します。このツールは、CloudLinuxの上限値をvCPUやRAMへ直接換算しません。

CloudLinuxを使うcPanelホスティングでは、一時点の値ではなくResource Usageの履歴から確認してください。繰り返す上限到達と発生時刻を記録し、アクセス、cron、バックアップ、インポート、管理作業と照合します。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="shared-hosting-diagnostic">
  <div class="mb-6">
    <label for="diag-evidence" class="form-label">判断材料の確かさ</label>
    <select id="diag-evidence" class="form-input">
      <option value="measured">管理画面の履歴・測定済みの指標</option>
      <option value="partial">一部の測定値がある</option>
      <option value="traffic">訪問者数・表示回数だけ</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="diag-memory" class="form-label">メモリ上限・PMEMの発生状況</label>
    <select id="diag-memory" class="form-input"><option value="0">なし</option><option value="1">時々</option><option value="2">繰り返し</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-cpu" class="form-label">CPU上限への到達</label>
    <select id="diag-cpu" class="form-input"><option value="0">なし</option><option value="1">時々</option><option value="2">繰り返し</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-ep" class="form-label">エントリープロセス・ワーカーの上限到達</label>
    <select id="diag-ep" class="form-input"><option value="0">なし</option><option value="1">時々</option><option value="2">繰り返し</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-nproc" class="form-label">プロセス数・NPROCの上限到達</label>
    <select id="diag-nproc" class="form-input"><option value="0">なし</option><option value="1">時々</option><option value="2">繰り返し</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-io" class="form-label">I/O・IOPSの負荷</label>
    <select id="diag-io" class="form-input"><option value="0">なし</option><option value="1">時々</option><option value="2">繰り返し</option></select>
  </div>
  <button class="btn btn-primary" type="submit">ボトルネックを診断</button>
</form>
<p id="shared-hosting-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">実際に確認できた状態を選んでください。</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("shared-hosting-diagnostic");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function value(id) { return Number(document.getElementById(id).value); }
    var memory = value("diag-memory");
    var cpu = value("diag-cpu");
    var ep = value("diag-ep");
    var nproc = value("diag-nproc");
    var io = value("diag-io");
    var evidence = document.getElementById("diag-evidence").value;
    var confidence = evidence === "measured" ? "高い" : (evidence === "partial" ? "中程度" : "低い");
    var repeated = [memory, cpu, ep, nproc, io].filter(function (v) { return v === 2; }).length;
    var findings = [];
    if (memory >= 1) findings.push("メモリ不足：ワーカーのメモリ、DBのワーキングセット、スワップ・OOM、バックグラウンドジョブを確認");
    if (cpu >= 1) findings.push("CPU負荷：vCPUを増やす前に、動的リクエストとDB処理の内訳を測定");
    if (ep >= 1) findings.push("ワーカー・同時処理の不足：処理時間を短縮し、キャッシュされない同時実行数を測定");
    if (nproc >= 1) findings.push("プロセス数の上限：容量を追加する前に、暴走・過剰なPHP、cron、バックグラウンドプロセスを特定");
    if (io >= 1) findings.push("ストレージの負荷：DBのI/O、バックアップ、ログ、インポートを確認。RAM増設だけでは解決しない場合があります");
    var decision;
    if (findings.length === 0) decision = "明確な容量不足の兆候はありません。測定で実際の制約が分かるまでは、現在のプランを維持するか、先に最適化してください。";
    else if (repeated >= 2) decision = "実測に基づいて移行・スペック選定：複数の上限に繰り返し達しています。明らかなソフトウェアの非効率を解消したうえで、VPSのスペックを検討する根拠があります。";
    else decision = "先に最適化して再確認：ボトルネックはありそうですが、ホスティングの一つの上限からVPSのスペックを直接決めることはできません。";
    document.getElementById("shared-hosting-result").textContent =
      decision + " 判定の確度：" + confidence + ". " + (findings.length ? findings.join("; ") + "." : "");
  });
});
</script>

共用サーバーの上限を、そのままVPSのスペックに置き換えないでください。CloudLinuxのCPU比率、エントリープロセス数、メモリ上限は、現在の環境の制限です。ボトルネックの手掛かりにはなりますが、VPSへ一対一で換算できる値ではありません。

代わりに、次の傾向を使います。

**CPUは正常だがメモリ上限に繰り返し達する：** vCPUを追加する前に、ワーカーとDBのメモリ、バックグラウンドジョブを調べます。

**必要な動的処理でCPU上限に繰り返し達する：** アプリとDBの処理内訳を測定し、その仕事量が本当に必要ならCPU追加を検討します。

**エントリープロセス・ワーカーが上限に達する：** 動的処理の同時実行数と処理時間を測ります。応答を速くすることで、サーバーを増強せずに待ち行列を解消できる場合があります。

**I/Oの負荷が高い：** RAMを増やせば直ると考える前に、バックアップ、ログ、DB処理、インポート、ストレージを多用するプラグインを特定します。

これにより、本当の容量不足と、非効率な一つの要素がホスティングの上限を引き起こしている状態を区別できます。

| 症状 | 確認すること | 先に最適化すること | 増強する目安 |
|---|---|---|---|
| メモリ上限・スワップ・OOM | プロセスメモリ、DBのワーキングセット、同時ワーカー | メモリリーク、大きすぎるワーカー、キャッシュ・DB設定 | 最適化後もRAMを使い切る |
| CPUの制限 | 継続的なCPU負荷とリクエスト・DBの処理時間 | 遅いコード、キャッシュされない処理、重いクエリ | 必要な処理が引き続きCPUに制約される |
| EP・ワーカーの待ち行列 | 動的な同時実行数と処理時間 | キャッシュ、遅いエンドポイント、ワーカー設定 | 処理負荷を下げても待ち行列が残る |
| I/O待ち・IOPS上限 | DB、ログ、バックアップ、インポート | 実行時刻、インデックス、ログ・バックアップの動作 | 通常の処理でもストレージ経路がボトルネックのまま |



## VPSの増強か、サイトの最適化か {#vps-or-website-optimization}

明らかなアプリの問題を修正した後も、必要な処理が繰り返しリソースを使い切る場合は、VPS増強の根拠になります。

次が負荷の原因なら、先に最適化します。

- 特定の遅いプラグイン・拡張機能。
- インデックスがない、または非効率なDBクエリ。
- ページ・オブジェクトキャッシュの不具合。
- 過剰なアクセスを行うボット。
- 暴走したcronジョブ。
- 大きすぎる画像の処理。
- ピーク時間帯に設定されたバックアップ・マルウェアスキャン。
- メモリリーク。
- 過剰なログ記録。

最適化後の負荷でも容量が不足すると測定で分かったら、サーバーのリソースを増やします。

この区別は費用面でも重要です。非効率なコードを共用サーバーから大きなVPSへ移すと、ボトルネックを取り除かず、一時的に隠すだけになることがあります。

## 同時実行数からPHP・アプリワーカーを選定 {#size-php-and-application-workers-from-concurrency}

サーバーは複数のリクエストを同時に処理するため、月間訪問者数だけでは選定の根拠として不十分です。

動的PHP処理では、稼働中の各ワーカーがリクエスト処理中にメモリとCPUを使います。そのため、対応できるワーカー数は、1個あたりの平均メモリと、処理が続く時間の両方に依存します。

RAMの簡易的な確認式は次のとおりです。

**ワーカー用RAMの配分＝基本サービス分を差し引いた利用可能RAM×ワーカーへ安全に割り当てられる割合**

この配分と実測したワーカーのメモリを比較します。DB、キャッシュ、OSのメモリが残らなくなるような、理論上の最大ワーカー数は設定しないでください。

キャッシュによって計算は変わります。ログインしていない利用者向けのキャッシュ済みページはPHPを完全に通らない場合がありますが、購入手続き、ログインセッション、wp-admin、API、個別表示ページはアプリに届きます。

WordPress固有の動作は[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})、取引を行うサイトの負荷は[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})をご覧ください。

## DBの要件がサーバーのスペックを決める場合もある {#database-demand-can-set-the-server-size}

CPU不足に見えても、根本の問題がDB処理にある場合があります。

次を確認してください。

- 遅いクエリの傾向。
- DBのワーキングセットの大きさ。
- クエリの同時実行数。
- 不足しているインデックス。
- 大きな自動読み込みデータや、それに相当するアプリのメタデータ。
- 負荷の高い検索・絞り込み・レポート処理。
- インポート・保守ジョブ。
- ストレージの遅延。

DBが大きなワーキングセットを必要とする場合、RAM増設は役立ちますが、非効率なクエリは直りません。CPU増強は処理量を増やせる一方、重いクエリが同時により多く競合する場合もあります。

## 平均ではなくピークのアクセスに備える {#plan-for-peak-traffic-not-average-traffic}

平均値で選定すると、利用者が実際に障害を経験する時間帯を見落とします。

キャンペーン開始、セール、メール配信、新商品の発売、定期インポート、バックアップ、cronの集中など、現実的に最も混む時間帯を特定します。その間に動的処理として残るリクエストと、ページキャッシュやCDNで処理できるものを見積もります。

次の処理が重なることを想定して余裕を確保します。

- 通常の利用者アクセス。
- ピーク時の動的処理。
- 管理作業。
- 定期ジョブ。
- デプロイ・キャッシュの事前生成。
- 監視・バックアップのプロセス。

CDNは静的配信や一部のオリジンへのリクエストを減らせますが、VPSに届く動的なアプリ・DB処理は残ります。

ピークの例：毎秒20リクエストのうち90%をキャッシュ・CDNで処理する場合、オリジンには毎秒約2件の動的リクエストが届きます。キャンペーンで合計が毎秒40件に倍増し、キャッシュ率が同じなら、アプリには毎秒約4件が届きます。p95の処理時間が0.8秒なら、管理ジョブや購入手続き・APIの急増を加える前で、約3.2件が同時に動的処理中になる目安です。

## ストレージ容量の選定 {#storage-sizing}

ディスク容量は、現在のサイトのディレクトリだけでは決まりません。

次を含めてください。

- サイトのファイル。
- データベース。
- アップロードされたメディア。
- ログ。
- 一時ファイル。
- パッケージ・アプリのキャッシュ。
- ローカルに置く場合はステージングのコピー。
- VPS上で一時作成する場合はバックアップファイル。
- 今後の増加分。

ファイルシステムを上限近くまで埋めないでください。DB、更新、ログ、バックアップには作業用の空き領域が必要です。

実用的には、次のように容量を見積もります。

**必要なディスク＝現在のファイル＋DB＋一時作業領域＋バックアップの一時保存領域＋予想増加分＋作業用の空き容量**

例：現在の使用量18 GB＋移行・更新の一時領域8 GB＋ローカルバックアップの一時領域18 GB＋予想増加分6 GBでは、安全のための余裕を加える前に40 GBを超えます。この場合は80 GBのほうが安全な開始構成です。容量はIOPSやストレージの遅延とは別です。ディスクを大きくしても、遅いDBが自動的に速くなるわけではありません。

## 帯域幅と月間転送量の見積もり {#bandwidth-and-monthly-transfer-sizing}

月間転送量はCPU、RAM、ポート速度とは異なります。処理性能に余裕があっても、大きなファイルやキャッシュされないメディアを直接配信すると、転送量の上限を超える場合があります。

大まかには、次の式で見積もれます。

**オリジンの月間転送量≈VPSから1リクエストあたりに送る平均バイト数×月間オリジンリクエスト数＋バックアップ・エクスポート・その他の送信**

より実用的には、キャッシュ可能な通信と動的通信を分けます。

**オリジン転送量≈要求された合計バイト数×（1－CDN・キャッシュが肩代わりする割合）＋キャッシュされない動的応答＋Web以外の送信**

例：利用者が1か月に2 TBのファイル・ページを要求し、その80%をCDNがオリジンに戻らず配信する場合、VPSはキャッシュ可能な通信の約400 GBに加え、動的ページ、API応答、バックアップ、エクスポート、キャッシュミス分を配信する可能性があります。

CDNでオリジンの転送量がゼロになるとは限りません。ログイン後のページ、購入手続き、API、キャッシュミス、キャッシュ削除、大容量ダウンロード、オリジンからCDNへの補充でも転送が発生します。また、**月間転送量の上限**と**ネットワークポート速度**を区別してください。ポート速度は可能な通信速度、転送量の上限は課金期間内に送れるデータ量を表します。

## 複数サイトでは計算が変わる {#multiple-websites-change-the-calculation}

1台のVPS上のサイトは、CPU、RAM、ストレージ、プロセスの処理能力を共有します。各サイトが小さくても、ピークが重なる場合があります。

合計の負荷でスペックを選び、一つのサイトのバックグラウンドジョブが他のリソースを奪わないだけの余裕を確保します。分離、障害の影響、リソース競合が重要になる場合は、1台を増強し続けるより処理を分けるほうが有効なことがあります。

複数サイトの判断は、[複数サイト向けVPS]({{< relref "vps-for-multiple-websites.md" >}})をご覧ください。

## 管理パネルとメールの消費量も含める {#control-panel-and-mail-overhead-belong-in-the-budget}

管理パネルはドメイン、SSL、DB、PHPバージョン、アカウントの管理を簡単にしますが、独自のサービスも動かします。サイトだけで計算せず、パネル用のメモリとストレージを確保してください。

メールを運用すると、SMTP、IMAP・POP、迷惑メール対策、ウイルススキャン、キュー、ログ、メールボックスが継続的にリソースを使います。VPSでサイトとメールを動かすなら、メールに追加負荷がないと考えず、RAM、CPU、ストレージ、バックアップの見積もりに含めます。

小規模サイトでは、メールを管理されたメールサービスに移すと、サーバー負荷と運用リスクを抑えられます。VPSに残す場合は、DNSレコード、事業者・IPの制約など、到達率に関わる要件を別に確認してください。VPSを大きくしても送信元の評価は改善しません。

パネルで管理したい場合は、[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})で利点と制約を比較できます。

## 繰り返し使えるVPS選定の手順 {#a-repeatable-vps-sizing-workflow}

1. **現在の負荷を測定する。** CPU、メモリ、動的処理の同時実行数、DBの動作、ストレージ、ピーク時間帯を記録します。
2. **ボトルネックを特定する。** CPU、RAM、ワーカー、DB、I/O、ソフトウェア制限の問題を分けます。
3. **明らかな非効率を取り除く。** 容量を購入する前に、キャッシュ、暴走ジョブ、非効率なクエリ、過剰なアクセスを修正します。
4. **リソースを見積もる。** 基本サービス、DB、アプリワーカー、管理パネル、バックグラウンド処理のRAMを確保します。
5. **余裕のある開始プランを選ぶ。** 余裕がない構成と、根拠なく過剰な容量を確保する構成の両方を避けます。
6. **現実的なピークを再現する。** 待機中のトップページだけでなく、本番を代表する動的処理の負荷で検証します。
7. **移行後も監視する。** 最初の見積もりを固定せず、実測に応じて調整します。本番運用の基本は[VPSの監視]({{< relref "vps-monitoring.md" >}})をご覧ください。

移行先のスペックが決まったら、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})で構成の洗い出し、非公開テスト、最終同期、DNS切り替え、切り戻しを計画します。

## 根拠に基づく構成の提案 {#evidence-based-recommendation}

有用なVPSの提案には、構成と、それを選ぶ理由の両方が必要です。

例えば、次のように示します。

**2 vCPU / 4 GB RAM / 80 GB**は、DBを使う企業向けCMSで、キャッシュされないPHP処理が相応にあり、管理パネルと運用上の余裕が必要な場合の開始構成として考えられます。一定の月間訪問者数に対応できるという保証ではありません。

訪問者数しか分からない場合、判断の確度は低くなります。CPUの履歴、メモリ不足、動的な同時実行数、ワーカーのメモリ、DBの動作、ストレージの増加が分かるほど、確度は高くなります。

確度は、次のように簡潔に示せます。

- **確度が低い：** 訪問者数、CMS名、おおまかなストレージ量だけ。
- **確度が中程度：** CPU・RAMの実測履歴の一部と、処理の種類、ピークの傾向がある。
- **確度が高い：** CPU・RAM・I/Oの時系列、キャッシュされない同時実行数、ワーカーのメモリ、処理時間、DBの動作、ストレージの増加が分かる。

確度が高いとは、前提がより確かだという意味であり、将来のアクセス数を保証するものではありません。

## 結果に合うVPSを選ぶ {#match-the-result-to-a-vps}

RAMの見積もり、CPUの実測、ストレージ容量、ピーク時の動作を合わせて判断します。以下のVDSina Standard構成は、結果をプランに対応させる例です。契約前に事業者の最新条件を確認してください。

| 構成 | 検討を始める際に適した用途 | 避ける・再確認する場面 | 主な検証項目 | 確認先 |
|---|---|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/日、1 TB/月 | テスト、ごく軽量なキャッシュ中心のサイト、最小限のサービス | パネル＋DB＋複数の動的ワーカー、本番ストア | RAMの余裕とディスク | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のプランを確認</a> |
| 1 vCPU / 2 GB / 40 GB — $0.50/日、32 TB/月 | 動的処理を抑えた軽量な小規模サイト・CMS | 継続的なCPU負荷、複数の稼働サイト、重いパネル・メール構成 | ワーカーとDBのメモリ、ストレージの増加 | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のプランを確認</a> |
| 2 vCPU / 4 GB / 80 GB — $0.67/日、32 TB/月 | 動的な企業向けCMS、中程度の非キャッシュPHP、パネル用の余裕 | 重いWooCommerce、大量インポート、高いDB負荷、複数サイトのピーク競合 | CPU飽和、DB遅延、ピークの重なり | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のプランを確認</a> |
| 4 vCPU / 8 GB / 160 GB — $1.34/日、32 TB/月 | 重い動的処理、大きなDB、複数の稼働サイト | 厳しい高可用性要件、非常に多い書き込み、個別の拡張が必要な処理 | 1台のVPSが引き続き適切な構成か | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のプランを確認</a> |

サイトが起動できるという理由だけで、1 GB・2 GBを本番の標準構成にしないでください。EC、大きなDB、複数の動的サイト、メール、管理パネルは余裕をすぐに消費する場合があります。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">VPSを選ぶ</a>
</p>

## VPSを契約する前に {#before-buying-the-vps}

スペック計算だけでは分からない提供条件も確認します。転送量、ストレージの種類と容量、IP、バックアップ、拡張方法、管理範囲、パネルのライセンス、現在の課金条件が対象です。CPU・RAMから最適な通信経路は決まらないため、設置場所は[VPSのリージョンの選び方]({{< relref "how-to-choose-vps-location.md" >}})で別に検討してください。

現在のサイトが共用サーバー上にある場合は、移行前に[VPSと共用サーバーの違い]({{< relref "vps-vs-shared-hosting.md" >}})で運用の変化を確認してください。

## 技術資料 {#technical-references}

- cPanel：サーバーのハードウェア要件
- cPanel：追加するRAM・CPU・ディスクの判断方法
- VDSina Standard VPSの構成

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のVPS提供内容を確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があります。提携リンクにはsponsoredを付けています。料金、転送量、その他の商用条件は変更される場合があるため、契約前に事業者のサイトで確認してください。</small></p>

## よくある質問 {#faq}

### Webサイト用VPSにRAMはどれくらい必要ですか？ {#how-much-ram-does-a-website-vps-need}

一律に信頼できる容量はありません。軽量なキャッシュ中心のサイトは少ないメモリで動く一方、DB、パネル、同時稼働ワーカーを持つ動的CMSでは大幅に多く必要になる場合があります。同時に動くプロセスから計算し、余裕を確保してください。

### Webサイト用VPSに2 GB RAMで十分ですか？ {#is-2-gb-ram-enough-for-a-website-vps}

小規模で軽量な負荷なら足りる場合があります。パネル、DB、複数のPHPワーカー、バックグラウンドジョブ、複数サイトを同時に動かすと制約になりやすくなります。RAM容量だけで判断せず、実際のメモリ使用状況を測定してください。

### 4 GB VPSはどのような用途に向いていますか？ {#what-does-a-4-gb-vps-tier-fit}

4 GB VPSは、Linux、DB、アプリ・PHPワーカー、キャッシュに余裕を持たせられるため、多くの企業向けCMSで実用的な出発点になります。適性は、動的な同時実行数、DB負荷、バックグラウンド処理、パネルの消費量によります。WordPress固有の判断は[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})をご覧ください。

### VPSは何人の訪問者に対応できますか？ {#how-many-visitors-can-a-vps-handle}

訪問者数だけでは答えられません。キャッシュヒット率、同時リクエスト数、アプリの実行時間、DB処理、バックグラウンドジョブによって、アクセス量が似たサイト同士でも処理能力に桁違いの差が出る場合があります。

### RAMとCPUのどちらを先に増やすべきですか？ {#should-i-add-ram-or-cpu-first}

測定で制約が確認されたリソースを増やします。メモリ不足、スワップ、OOMはRAMまたはメモリ最適化の必要性を示します。最適化済みの必要な処理でCPU飽和が続くならCPUが候補です。DBとI/Oのボトルネックは別に診断します。

### CDNでVPSの必要スペックは下がりますか？ {#does-a-cdn-reduce-vps-requirements}

静的ファイルの配信や、キャッシュ可能なオリジンへのリクエストは減らせます。オリジンへ届く動的アプリリクエストとDB処理は、引き続きVPSのリソースを使います。

### 平均とピークのどちらのアクセスに合わせるべきですか？ {#should-i-size-for-average-or-peak-traffic}

現実的なピークに運用上の余裕を加えて選びます。平均値だけでは、同時処理、定期ジョブ、動的リクエストが重なる短時間の負荷を見落とすことがあります。
