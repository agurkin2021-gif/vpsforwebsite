---
title: "VPSと共用サーバーの違い"
description: "VPSと共用サーバーを、リソース制限、自由度、管理責任、総費用、移行の準備から比較。現状維持・先に最適化・VPS移行のどれが適切か判断できます。"
image: "images/home/vps-for-website-hero.webp"
slug: "vpsと共用サーバーの違い"
---

VPSと共用サーバーは、単純に「小規模サイトか大規模サイトか」で選ぶものではありません。共用サーバーは事業者がサーバー環境を運用するため、通常は手軽です。VPSは自由度が高く、より分離された仮想環境を使えますが、利用者か管理者が仮想サーバー内を運用する必要があります。

多くの場合、適切な判断は**共用サーバーを継続、先に最適化、VPSへ移行、管理支援を確保して移行**の4つに分かれます。

契約までの全体の考え方は、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[比較表](#quick-comparison) · [判断チェック](#shared-hosting-vs-vps-decision-checker) · [継続](#stay-on-shared-hosting-when) · [先に最適化](#optimize-first-when-the-site-is-the-bottleneck) · [移行](#move-to-vps-when) · [費用](#compare-total-operating-cost) · [よくある質問](#faq)

## 比較表 {#quick-comparison}

| 判断項目 | 共用サーバー | VPS |
|---|---|---|
| サーバー管理 | 通常は事業者がOS・ホスティング環境を管理 | 管理サービスで別途定められていない限り、利用者・管理者がゲストOSを管理 |
| root・管理者権限 | 通常は利用不可、または制限あり | 通常は利用可能 |
| ソフトウェア・実行環境 | 事業者が対応する構成に限定 | 大幅に柔軟 |
| リソースの仕組み | 共有基盤内でアカウントごとに割り当て・上限を設定 | プランに応じて仮想CPU・RAM・ストレージを割り当て |
| 分離 | 多数のアカウントが同じ管理環境を共有 | ゲスト・アカウントの分離は強まるが、仮想化された基盤であることは変わらない |
| 管理パネル | 通常はホスティングに含まれる | 任意。別途インストールする場合あり |
| メール・DNS | 一体で提供されることが多い | 別途設定や外部サービスが必要な場合あり |
| バックアップ | プランに含まれる場合あり | 明示的に含まれない限り、利用者が復旧手段を確認・設定 |
| 監視 | 事業者が基盤を監視。サイト単位の確認範囲は異なる | 通常は利用者・管理者がゲストOSとサービスを監視 |
| 費用 | ホスティング料金としてまとまりやすい | VPSに加え、パネル・バックアップ・監視・メール・管理時間の費用が発生し得る |
| 適した用途 | 対応する構成と上限に収まるシンプルなサイト | 自由度、独自ソフトウェア、より強い分離、柔軟なリソース計画が必要なサイト |

どちらかが常に優れているわけではありません。

## 共用サーバーとVPSの判断チェック {#shared-hosting-vs-vps-decision-checker}

次に取るべき行動を確認するためのツールです。「サイトが遅いからVPSを買う」と即断せず、必要性を慎重に判断します。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="shared-vs-vps-checker">
  <div class="mb-6">
    <label for="sv-limits" class="form-label">必要な処理でリソース上限に繰り返し達していますか？</label>
    <select id="sv-limits" class="form-input">
      <option value="no">いいえ・未測定</option>
      <option value="occasional">時々ある</option>
      <option value="repeated">通常の必要な処理で繰り返し発生</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="sv-custom" class="form-label">共用プランでは使えないroot権限、独自の実行環境・ソフトウェア、ワーカー、サービスが必要ですか？</label>
    <select id="sv-custom" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sv-optimized" class="form-label">明らかなサイト側の問題を先に確認しましたか？</label>
    <select id="sv-optimized" class="form-input">
      <option value="no">いいえ。キャッシュ・プラグイン・クエリ・ボット・ジョブは未確認</option>
      <option value="yes">はい。主な非効率を調査済み</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="sv-admin" class="form-label">VPSを運用できる担当者はいますか？</label>
    <select id="sv-admin" class="form-input">
      <option value="no">いいえ</option>
      <option value="help">有料管理支援・マネージドサービスがあれば対応可能</option>
      <option value="yes">はい。社内の担当者がいる</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="sv-critical" class="form-label">ホスティング障害の損失はどれくらいですか？</label>
    <select id="sv-critical" class="form-input">
      <option value="low">小さい。趣味・テスト・重要度の低いサイト</option>
      <option value="medium">中程度。通常の事業用サイト</option>
      <option value="high">大きい。売上・業務が依存している</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="sv-stable" class="form-label">その他の点では、現在の共用サーバーは安定し、サイトの要件を満たしていますか？</label>
    <select id="sv-stable" class="form-input"><option value="yes">はい</option><option value="no">いいえ</option></select>
  </div>
  <button class="btn btn-primary" type="submit">次の行動を確認</button>
</form>
<p id="shared-vs-vps-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">可能な限り、現在のホスティングの実際の動作を基に答えてください。</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("shared-vs-vps-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var limits = document.getElementById("sv-limits").value;
    var custom = document.getElementById("sv-custom").value === "yes";
    var optimized = document.getElementById("sv-optimized").value === "yes";
    var admin = document.getElementById("sv-admin").value;
    var critical = document.getElementById("sv-critical").value;
    var stable = document.getElementById("sv-stable").value === "yes";

    var result;

    if (!custom && limits !== "repeated" && stable) {
      result = "共用サーバーを継続：基盤を変更すべき明確な兆候はまだありません。管理が簡単な現在の方式を維持し、実際のリソース使用状況を監視してください。";
    } else if (!optimized && !custom) {
      result = "まず最適化・共用環境を再確認：VPSを契約する前に、キャッシュ、遅いプラグイン・クエリ、ボット、cronジョブなど、アプリ側の原因を調べてください。";
    } else if ((custom || limits === "repeated") && admin === "yes") {
      result = "VPSへ移行：機能やリソース面で実際の理由があり、運用担当者もいます。実測からスペックを選び、移行を計画してください。";
    } else if ((custom || limits === "repeated") && (admin === "help" || critical === "high")) {
      result = "管理支援を利用して移行：基盤を変える理由はありますが、事業上のリスクや運用担当の不足を考えると、自己管理だけでの移行は適していません。";
    } else if (custom || limits === "repeated") {
      result = "運用の担当を決めてから移行：基盤を変える理由はありますが、現在はサーバー作業の担当者がいません。本番を切り替える前に、マネージドサービスや有料の管理代行を手配してください。";
    } else {
      result = "現在のプランを再検討：判断材料が混在しています。VPS管理の負担を引き受ける前に、より適した共用プランやマネージド型のアプリホスティングを比較してください。";
    }

    document.getElementById("shared-vs-vps-result").textContent = result;
  });
});
</script>

## 共用サーバーからVPSへ移ると何が変わるか {#what-actually-changes-between-shared-hosting-and-vps}

最大の違いは、料金表のスペックの数字ではなく、**運用体制**です。

### 共用サーバー {#shared-hosting}

通常は事業者が基盤となるホスティング環境を管理・保守します。次のものが提供されます。

- サポート対象の実行環境。
- アカウントごとの割り当てと、プロセス・リソース上限。
- ホスティング用の管理パネル。
- 事業者によるサーバー保守。
- 多くの場合、メール・DNS・バックアップなどの機能。

サーバーレベルの自由度と引き換えに、手軽さを得られます。

### VPS {#vps}

割り当てられたリソースと管理権限を持つ仮想サーバーを利用できます。

通常は次を自分で制御できます。

- OS。
- パッケージ。
- Webサーバー。
- PHP・実行環境のバージョン。
- データベース。
- バックグラウンドワーカー。
- ファイアウォール。
- 独自のサービス。
- 管理パネルの選択。

ただし、自己管理型VPSでは、これらの管理責任も利用者に移ります。

VPSは仮想化された基盤です。対象製品に明記されていない限り、専用の物理ハードウェアとは考えないでください。

## 共用サーバーを継続する場面 {#stay-on-shared-hosting-when}

次の場合は、共用サーバーが引き続き適した選択です。

- サイトが安定している。
- 必要な処理でリソース上限に繰り返し達していない。
- 必要なPHP・実行環境・DBにすでに対応している。
- 長時間稼働するサービスや独自サービスが不要。
- root権限が不要。
- メール・DNS・管理パネルの一体提供が便利。
- チームでサーバー運用を担当したくない。
- 現在のプランが性能と信頼性の要件を満たしている。

新しいブログ、ポートフォリオ、案内サイト、小規模事業のサイトは、適切な共用サーバーを長く利用できる場合があります。

「VPSのほうが速そう」という理由だけで移行すると、確認済みの問題を解決せずに作業だけが増えます。

## サイト自体がボトルネックなら先に最適化 {#optimize-first-when-the-site-is-the-bottleneck}

サイトが遅いだけでは、共用サーバーの容量不足だとは判断できません。

まず次を確認します。

- 遅いプラグイン・拡張機能。
- 重いDBクエリ・インデックスがないクエリ。
- ページ・オブジェクトキャッシュの不具合。
- 過剰なアクセスを行うボット。
- 暴走したcronジョブ。
- 大きすぎる画像の処理。
- 外部APIの遅延。
- 過剰なログ記録。
- アクセスのピークに重なるバックアップ・セキュリティスキャン。
- メモリリーク。
- フロントエンドの重さ。

ホスティングのCPU・メモリ・プロセスの指標が低いままサイトが遅い場合、同じソフトウェアの問題を、自分で管理する必要があるサーバーへ移すだけになる可能性があります。

詳しいボトルネックの診断は、[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})をご覧ください。

## VPSへ移行する場面 {#move-to-vps-when}

非効率な一つの要素ではなく、ホスティング方式そのものが制約になっている場合、VPSを選ぶ根拠があります。

有力な兆候は次のとおりです。

- 必要な負荷でCPU・メモリ・プロセス数・I/Oの上限に繰り返し達する。
- root・管理者権限が必要。
- Webサーバーの独自設定が必要。
- 現在の環境が必要なPHP・実行環境のバージョンに対応していない。
- バックグラウンドワーカーや長時間動くプロセスがある。
- 独自のDB・サービス要件がある。
- 共用環境では許可されていないソフトウェアを使う。
- 処理環境をより強く分離する必要がある。
- 複数サイト・サービスを一つの管理下に置く必要がある。
- ファイアウォール・ネットワーク・サービスの設定を制御したい。

アクセス量だけでは十分な判断材料になりません。

## アクセス量以外の機能要件 {#capability-triggers-beyond-traffic}

アクセスが少ないサイトでも、VPSが必要な場合があります。

例えば、次の要件です。

- 常駐サービスが必要なNode.js・Pythonアプリ。
- キューワーカー。
- 共用サーバーの上限を超える定期インポート。
- Redisなどの必須サービス。
- 独自のリバースプロキシ。
- 構成に適している場合のDocker・コンテナ。
- 特定の実行環境のバージョン。
- 独自のファイアウォール・ネットワーク動作。
- サーバーレベルでの動作状況の把握。

VPSを選ぶ理由は、成長ではなく**必要な機能**にある場合もあります。

## 共用サーバーの上限はVPSのスペックではない {#shared-limits-are-not-vps-specifications}

共用サーバーとVPSでは、処理能力の表し方が異なります。

共用サーバーでは、次の指標が表示されることがあります。

- CPUの割合。
- 物理メモリ・PMEM。
- エントリープロセス数。
- プロセス数・NPROC。
- I/O・IOPS。
- DB接続数の上限。

VPSではリソースを割り当てられ、その範囲で次の構成を設定します。

- アプリケーションワーカー。
- PHP-FPMプール。
- DB用メモリ。
- キャッシュ。
- バックグラウンドジョブ。
- Webサーバー。
- 管理パネル・メールサービス。

「共用CPU 100%」を「1 vCPU VPS」へ、エントリープロセスの上限をワーカー数へ、直接置き換えないでください。

共用環境の上限到達履歴でボトルネックを特定し、実際の負荷からVPSを選びます。詳しい読み替え方は、[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})で説明します。

## VPSなら必ず速くなるわけではない {#vps-is-not-automatically-faster}

適切に運用された共用環境は、設定やスペックが不適切なVPSより高い性能を発揮する場合があります。

次の場合、VPSのほうが遅くなることがあります。

- RAM不足でスワップやプロセスの強制終了が発生する。
- PHP・アプリワーカーの設定が不適切。
- DBの設定が不適切。
- キャッシュがない。
- Webサーバーの設定が誤っている。
- バックアップ・インポートが利用者の処理と競合する。
- アプリ自体が非効率。

VPSで得られるのは、**自由度と異なるリソース・管理の仕組み**であり、速度の保証ではありません。

## 管理責任が変わる {#administration-responsibility-changes}

共用サーバーでは、サーバー管理の大部分を利用者が担当せずに済みます。

アンマネージドVPSでは、次を誰かが担当します。

- OS・パッケージの更新。
- SSH・RDPの接続方針。
- ファイアウォール。
- Webサーバー。
- PHP・実行環境。
- データベース。
- バックアップ。
- 復元テスト。
- 監視。
- ログ。
- TLS。
- 障害対応。

利用者側に担当者がいない場合、選択肢は「共用か自己管理VPSか」ではなく、**共用か、マネージドVPS・有料管理代行か**になることがあります。

責任の境界は、[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})をご覧ください。

## セキュリティ・バックアップ・監視の担当 {#security-backups-and-monitoring-ownership}

共用サーバーでは、運用の多くが利用者から見えない形で行われます。VPSでは、その運用部分にも向き合う必要があります。

移行前に、次の担当者を決めてください。

- OS・パッケージのセキュリティ更新。
- SSH・管理者接続の方針。
- ファイアウォール・サービスの公開範囲。
- バックアップジョブの失敗対応。
- 復元テスト。
- ディスク・メモリ・CPUの通知。
- 外部からのサイト死活監視。
- TLSの更新。
- ログの確認。
- 障害対応。

物理・仮想化基盤は引き続き事業者の担当ですが、アンマネージドVPSのゲストOSとサイトの実行環境は、一般に利用者の責任です。

担当が決まっていないままVPSへ移行すると、基盤の柔軟性は増えても、運用リスクが高まる場合があります。

## 共用サーバーから移る際に代替が必要なサービス {#shared-hosting-services-you-may-have-to-replace}

共用サーバーには、Webサーバーの処理能力以外も含まれていることがよくあります。

解約前に、次を洗い出してください。

- 管理パネル。
- メールボックス。
- SMTP。
- DNSホスティング。
- 自動バックアップ。
- マルウェア・セキュリティスキャン。
- ステージング。
- CMSの簡単インストール機能。
- PHP・DBの問題へのサポート。
- SSLの自動設定・更新。
- 統計・ログの閲覧機能。

VPSには、同等の機能が自動で含まれるとは限りません。

ホスティング用の管理画面が重要なら、[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})を比較してください。

メールはVPSへ移すか、管理されたメールサービスに残すかを判断します。

## 運用の総費用を比較 {#compare-total-operating-cost}

共用サーバーの請求額とVPS本体の料金だけを比較しないでください。

次のように考えます。

**VPSの総運用費＝サーバー＋パネル・ライセンス＋バックアップ保存先＋監視＋メール＋管理時間＋障害対応・復旧費**

共用サーバーは事業者が運用作業を引き受けるため、月額請求がVPS本体より高くても、全体では経済的な場合があります。

次の場合はVPSのほうが経済的になる可能性があります。

- サーバー管理のスキルをすでに社内で持っている。
- 独自サービスや制御が実際に必要。
- 複数の処理を安全に集約できる。
- 制約のある共用プランを繰り返し上げるより、必要なリソース構成を安く確保できる。

初回の割引料金だけでなく、更新時・通常運用時の料金を比較してください。

## 共用サーバーと自己管理VPSの中間の選択肢 {#middle-paths-between-shared-hosting-and-raw-vps}

選択肢は二つだけではありません。

自己管理だけのVPSへ移る前に、次も検討します。

- 共用サーバーの上位プラン。
- マネージドWordPress・アプリホスティング。
- マネージドVPS。
- 管理パネルを使う自己管理型VPS。
- 自己管理型VPSと、有料・オンコールの管理支援。
- 基盤を変える前のサイト最適化。

制約を実際に解消できる範囲で、運用の変化が最小になる方法を選んでください。

## 移行の準備 {#migration-readiness}

共用サーバーから離れる前に、移行先のプランで現在使っているサービスとソフトウェアを扱えるか確認します。

次を洗い出します。

- 実行環境のバージョン。
- PHPの拡張・モジュール。
- DBエンジン・バージョン。
- cron・定期ジョブ。
- ストレージ。
- DNS。
- SSL。
- メール。
- メール関連のDNSレコード。
- 外部のWebhook・API。
- バックアップ。
- 切り戻し手順。

最初のコピーが終わっただけで、共用サーバーを解約しないでください。

実際の切り替え手順は、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})をご覧ください。

契約後に手動で公開する方法は、[VPSでWebサイトを公開する方法]({{< relref "how-to-host-a-website-on-vps.md" >}})で説明します。

## VPSとSEO {#vps-and-seo}

VPSへの変更は、Googleの順位を直接上げる近道ではありません。

共用サーバーが応答の遅さ・不安定さの原因で、VPSを正しく設定できるなら、移行で利用体験が改善する場合があります。ただし、サーバーの種類を変えるだけで順位が上がるわけではありません。

SEO上の目標も具体的に考えます。

- 安定したHTTP応答。
- 許容できるサーバー応答時間。
- 正しいリダイレクト。
- HTTPS。
- 意図しないnoindex・robotsの変更を起こさない。
- 移行中の停止・データ損失を防ぐ。

基盤は性能と信頼性を支えますが、アプリ改善やSEOの作業に代わるものではありません。

## VPSを選ぶ前に {#before-choosing-the-vps}

判断チェックでVPSへの移行が示されたら、次を確認します。

1. 理由が**容量、機能、分離**のどれかを明確にする。
2. サーバーの管理担当を決める。
3. 実際の負荷からCPU・RAM・ストレージを選ぶ。
4. パネルか手動構築かを決める。
5. メール・DNS・バックアップを洗い出す。
6. 移行と切り戻しを計画する。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のVPS構成を確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で申し込むと当サイトが報酬を受け取る場合があります。当ページでは、処理負荷や必要な機能が運用の変更に見合う場合にのみVPSを勧めています。</small></p>

## よくある質問 {#faq}

### VPSは共用サーバーより優れていますか？ {#is-vps-better-than-shared-hosting}

常にそうとは限りません。サーバーレベルの制御、独自ソフトウェア、より強い分離、共用環境では得られないリソース構成が必要ならVPSが適しています。手軽さや事業者によるサーバー運用を重視するなら、共用サーバーのほうが適する場合が多いです。

### VPSは共用サーバーより必ず速いですか？ {#is-vps-always-faster-than-shared-hosting}

いいえ。適切な共用環境は、設定やスペックが不適切なVPSより速い場合があります。性能はアプリ、キャッシュ、DB、Web環境、リソース選定によって変わります。

### 共用サーバーからVPSへいつ移行すべきですか？ {#when-should-i-move-from-shared-hosting-to-vps}

必要な処理が繰り返し上限に達する、または必要な機能を共用環境内で実現できず、サーバー管理の担当者がいる場合に移行します。

### サイトが遅ければVPSへ移るべきですか？ {#should-i-move-to-vps-if-my-website-is-slow}

まずサイト自体を確認してください。遅いプラグイン、クエリ、キャッシュ不足、ボット、バックグラウンドジョブは、移行しても遅いままの場合があります。

### 共用環境のCPU・エントリープロセス数をVPSのスペックに換算するには？ {#how-do-i-convert-shared-hosting-cpu-or-entry-processes-into-vps-size}

一対一では換算しません。共用環境の指標でボトルネックを特定し、実際の同時処理数、ワーカーのメモリ、DB負荷、ピークからVPSを計算します。

### VPSに管理パネルは含まれますか？ {#does-vps-include-a-control-panel}

含まれるとは限りません。VPSは手動でも管理パネルでも運用できます。事業者が提供するイメージとライセンスの条件を確認してください。

### 共用サーバーとVPSではメール運用がどう違いますか？ {#how-does-email-hosting-differ-between-shared-hosting-and-vps}

共用サーバーはアカウントにメールボックスを含むことがよくあります。VPS本体には管理されたメールが含まれない場合があるため、自分でメールサービスを運用するか、別の管理されたサービスに残すかも比較に含めます。

### VPSには技術的なスキルが必要ですか？ {#do-i-need-technical-skills-for-vps}

アンマネージドVPSには必要です。更新、セキュリティ、バックアップ、監視、障害対応を誰かが担当しなければなりません。担当できない場合は管理代行を利用するか、事業者が管理する環境を継続してください。

### VPSへの移行でSEOは改善しますか？ {#does-moving-to-vps-improve-seo}

直接の効果はありません。ホスティングがボトルネックなら性能・信頼性が改善する場合はありますが、サーバーの種類だけで順位は保証されません。

### 移行を決めた後は何をすべきですか？ {#what-should-i-do-after-deciding-to-move}

スペックを選び、管理代行・手動・パネルの管理方法を決め、移行先を準備します。サイトをテストし、データを移し、DNSを慎重に切り替え、切り戻し手順を残してください。
