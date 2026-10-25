---
title: "VPSのセキュリティチェックリスト"
description: "VPSのセキュリティチェックリスト。管理アクセス、ファイアウォール、更新、秘密情報、バックアップ、障害対応を順に確認し、締め出しを防ぎながら保護を強化します。"
image: "images/home/vps-for-website-hero.webp"
slug: "vpsのセキュリティチェックリスト"
---

このVPSセキュリティチェックリストは、インターネットに公開する自己管理型サーバーを、優先順位に沿って保護するためのものです。「100%安全」にすることが目標ではありません。不要な攻撃対象を減らし、特権アクセスを保護し、ソフトウェアを保守し、復旧できるようにして、セキュリティ作業に実際の担当者がいることを確認します。

安全に進めるには順序が重要です。**まず復旧経路を確保し、別の管理ログインを確認し、公開サービスを把握してから、SSHとファイアウォールを制限します**。

パッチ、ファイアウォール方針、バックアップ検証、監視、障害対応の担当者がいなければ、先に運用体制を整えてください。[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})をご覧ください。

サーバー選び全体の考え方は、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[対策の順序](#security-baseline-in-order) · [チェックツール](#vps-security-baseline-checker) · [SSH](#harden-administrative-access) · [ファイアウォール](#firewall-only-the-services-you-need) · [更新](#patching-and-automatic-security-updates) · [バックアップ](#backups-are-a-security-control) · [侵害への対応](#after-a-suspected-compromise) · [よくある質問](#faq)

## 基本的なセキュリティ対策の順序 {#security-baseline-in-order}

一般的な公開Linux VPSでは、次の順序で進めます。

1. **事業者のコンソール・復旧アクセスを使える状態に保つ。**
2. **個人を識別できる非rootの管理ユーザーを作成し、テストする。**
3. **SSH鍵認証を設定し、別セッションでログインできるか確認する。**
4. **待ち受け中の全サービスと公開ポートを一覧にする。**
5. **鍵でアクセスできてから、SSHのroot・パスワード方針を制限する。**
6. **原則拒否のファイアウォールを設定し、必要なポートだけを開く。**
7. **データベース、Redis、内部アプリケーション用ポートは原則非公開にする。**
8. **OS・パッケージのセキュリティ更新を適用し、再起動の担当を決める。**
9. **パネル、CMS、プラグイン、実行環境、依存ライブラリも更新する。**
10. **秘密情報を保護し、ユーザー・DBアカウントに最小権限を適用する。**
11. **多層防御として総当たり攻撃対策とレート制限を追加する。**
12. **公開サイトはHTTPSを使い、管理画面を保護する。**
13. **独立したバックアップを保持し、復元をテストする。**
14. **セキュリティ・復旧の失敗を把握できるログと通知を有効にする。**
15. **侵害が疑われた場合の対応を決める。**
16. **定期的に監査を繰り返す。**

内容を理解せずコマンドを貼り付けてリモートアクセスを制限しないでください。正当な管理者を締め出す変更も、サービス停止の原因になります。

## VPSの基本セキュリティ対策チェック {#vps-security-baseline-checker}

基本対策の不足を見つけるツールです。サーバーの安全性を認証するものではありません。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-security-checker">
  <div class="mb-6">
    <label for="sec-recovery" class="form-label">事業者のコンソール・復旧経路をテスト済み？</label>
    <select id="sec-recovery" class="form-input"><option value="no">いいえ・不明</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-admin" class="form-label">個人用の非root管理ユーザーでSSH鍵ログインを確認済み？</label>
    <select id="sec-admin" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-firewall" class="form-label">ファイアウォールが有効で、必要な公開ポートだけを許可している？</label>
    <select id="sec-firewall" class="form-input"><option value="no">いいえ・不明</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-services" class="form-label">待ち受けサービスと公開ポートを把握済み？</label>
    <select id="sec-services" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-updates" class="form-label">OS・アプリの更新担当とサービス・OS再起動の手順がある？</label>
    <select id="sec-updates" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-backup" class="form-label">独立したバックアップがあり、復元をテスト済み？</label>
    <select id="sec-backup" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-logs" class="form-label">セキュリティ・復旧の失敗を記録・通知し、確認する人がいる？</label>
    <select id="sec-logs" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-app" class="form-label">CMS・パネル・実行環境・依存関係の更新担当がいる？</label>
    <select id="sec-app" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-owner" class="form-label">セキュリティ事故の担当者・チームが決まっている？</label>
    <select id="sec-owner" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <button class="btn btn-primary" type="submit">基本対策を確認</button>
</form>
<p id="vps-security-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">実装して動作確認した対策だけを「はい」にしてください。</p>
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
      result = "重大な不足あり：特権アクセス、ファイアウォール・更新、復旧、または障害対応の担当が未整備です。本番運用の基本的なセキュリティ対策が完了したとは考えないでください。";
    } else if (missing.length > 0) {
      result = "基本対策は未完了：主要な対策はありますが、未解決のチェック項目が" + missing.length + "件あります。設定ファイルだけでなく、対策が実際に動作することを確認してください。";
    } else {
      result = "本番運用の基本対策を確認済み：一覧の対策は実装・テストされています。ただし、安全性を保証するものではありません。更新、監視、バックアップテスト、定期監査を続けてください。";
    }

    document.getElementById("vps-security-result").textContent = result;
  });
});
</script>

## アクセス変更の前に復旧経路を確保する {#keep-a-recovery-path-before-changing-access}

SSHを制限したり厳格なファイアウォールを有効にしたりする前に、誤ったルールから復旧できることを確認します。

事業者のブラウザーコンソール、VNC、復旧画面など、通常のネットワーク接続とは別の経路を少なくとも1つ確保してください。

そのうえで、次を計算します。

1. 個人を識別できる管理ユーザーを作成します。
2. SSH公開鍵を追加します。
3. **別の**ターミナルセッションを開きます。
4. ログインとsudo・管理者権限を確認します。
5. 新しい方針をテストする間、動作中のセッションを開いたままにします。
6. 確認できてから古いアクセス方法を制限します。

重要なのは、rootを急いで無効にすることではありません。**締め出しを起こさず、危険なアクセス方法を確認済みの安全な経路に置き換えること**です。

初回構築の流れは、[VPSでWebサイトを公開する方法]({{< relref "how-to-host-a-website-on-vps.md" >}})をご覧ください。

## 遮断する前に公開サービスを把握する {#inventory-exposed-services-before-blocking}

開いているポートを推測だけで判断しないでください。

Linuxでは、次のようなツールで待ち受けソケットを確認します。

```bash
sudo ss -lntup
```

各待ち受けサービスについて、次を判断します。

- そのサービス自体が必要か。
- 全インターフェースで待ち受ける必要があるか。
- 公開する必要があるか。
- localhostまたはプライベートネットワークだけにバインドできるか。
- どの送信元ネットワークから接続を許可するか。
- 誰が更新とログを担当するか。

一般的な公開サイトでは、次のポートを使う場合があります。

- SSH・管理アクセス。
- HTTP 80。
- HTTPS 443。

ただし、すべてのサーバーでこの3種類をインターネット全体に公開すべきという意味では**ありません**。

ファイアウォールで隠すだけでなく、使わないサービスは削除してください。

## 管理アクセスを保護する {#harden-administrative-access}

UbuntuのOpenSSHドキュメントでは公開鍵認証を扱い、Ed25519などの新しい鍵アルゴリズムを推奨しています。

基本の管理方式は次のとおりです。

- 個人を識別できる管理アカウント。
- SSH鍵認証。
- 可能な範囲で秘密鍵をパスフレーズで保護。
- 必要なユーザーだけにsudoを許可。
- アプリケーションをrootで動かさない。
- 安全な経路を確認してから、root直接ログイン・パスワードSSHを制限。

より高い保証が必要な環境では、OpenSSHでFIDO/U2FやTOTPベースの二要素認証なども利用できます。

### rootログインとパスワード認証 {#root-login-and-password-authentication}

鍵でのアクセスとコンソール復旧を確認する前に、これらの設定を無条件に変更しないでください。

安全な経路が動作したら、次を見直します。

- `PermitRootLogin`。
- `PasswordAuthentication`。
- `AllowUsers` / `AllowGroups`。
- 必要に応じたアイドル時間・セッション方針。

具体的な方針は環境によって異なります。

SSHをポート22から変えるとスキャンのノイズを減らせる場合がありますが、鍵、最小権限、ファイアウォール方針、ソフトウェア保守の**代わりにはなりません**。

## ファイアウォール：必要なサービスだけを許可する {#firewall-only-the-services-you-need}

Ubuntuの標準的なホストファイアウォール用フロントエンドはUFWです。

基本の考え方は次のとおりです。

- 要求していない受信通信は原則拒否。
- 実際に使う管理経路を許可。
- 公開WebサーバーではHTTP/HTTPSを許可。
- データベースと内部サービスは非公開。
- IPv4とIPv6の両方の動作を確認。

制限の厳しいルールを有効にする前に、SSHアクセスを確保してください。

確認コマンドの例：

```bash
sudo ufw status verbose
```

構成が異なる場合、一般的な「22/80/443を許可」という一覧をそのまま使わないでください。

### 事業者のファイアウォールとホスト側のファイアウォール {#provider-firewall-and-host-firewall}

事業者・ネットワーク側のファイアウォールは、仮想マシンに届く前に通信を遮断できます。

ホスト側のファイアウォールは、ゲストOSが受け入れる通信を制御します。

両方を使う多層防御は有効ですが、ルールを文書化し、互いに矛盾しないようにする必要があります。

## データベースと内部サービスは原則非公開にする {#keep-databases-and-internal-services-private-by-default}

サービスが待ち受けているという理由だけで、MySQL/MariaDB/PostgreSQL、Redis、内部のNode・Python用ポート、制御ソケットを公開しないでください。

次を優先します。

- 同じサーバー内のサービスにはlocalhost。
- 複数サーバー構成にはプライベートネットワーク。
- リモート管理が必要な場合は送信元IPの制限。
- 管理作業にはSSH・VPN・踏み台経由のアクセス。

データベースのポートを公開するのは、構成上必要で、アクセスを厳しく制限できる場合に限ります。

## パッチ適用とセキュリティ更新の自動化 {#patching-and-automatic-security-updates}

サポート中のOSでも、更新の担当者がいなければ古くなります。

対応するUbuntu Serverのインストールでは、標準で`unattended-upgrades`によるセキュリティ自動更新を利用します。

便利な仕組みですが、運用では次も確認する必要があります。

- どのリポジトリーが対象か。
- 外部パッケージやアプリも更新されるか。
- サービスの再起動が必要になったか。
- OSの再起動が必要か。
- 誰が更新失敗を確認するか。
- 本番サービスをいつ安全に再起動できるか。

Ubuntuのドキュメントでも、更新したコードを有効にするには、サービスの再起動や、場合によってはOS再起動が必要と説明されています。

自動更新を有効にするだけで、パッチ管理全体が完了したと考えないでください。

## Fail2ban・CrowdSec・レート制限 {#fail2ban-crowdsec-and-rate-limiting}

総当たり攻撃への対策ツールは、繰り返しの不正な試行を減らすのに役立ちます。

これらは**多層防御**であり、中心となる認証方式ではありません。

次を整えてから使います。

- 特権アクセスを保護している。
- 強固な認証を導入している。
- 公開サービスを意図的に選んでいる。
- ログを利用できる。

遮断ツールがあっても、弱いパスワード、未更新のパネル、公開されたDBが安全になるわけではありません。

## アプリケーションとDBに最小権限を適用する {#least-privilege-for-applications-and-databases}

最小権限の原則は構成全体に適用します。

次を優先します。

- デプロイ用と管理用のユーザーを分ける。
- アプリケーションごとにユーザーを分ける。
- アプリケーションごとにDBユーザーを分ける。
- 必要なDB権限だけを与える。
- 関係のない顧客サイトは別ユーザーにする。
- 書き込み可能なディレクトリーを必要な範囲に限定する。

次は避けます。

- Webアプリケーションをrootで実行する。
- DBのroot・管理者アカウントをアプリケーションと共有する。
- 権限問題を`chmod 777`で解決しようとする。
- 分離できるのに、無関係な顧客サイトを同じUnixユーザーで動かす。

複数サイトの分離は、[複数サイト向けVPS]({{< relref "vps-for-multiple-websites.md" >}})をご覧ください。

## 秘密情報と認証情報を保護する {#protect-secrets-and-credentials}

本番の認証情報を、次の場所に置かないでください。

- 公開Gitリポジトリー。
- Webからアクセスできるドキュメントルート。
- デバッグページ。
- スクリーンショット・問い合わせ・チャット。
- 可能な限りシェル履歴。
- 広く読み取り可能な環境変数ファイル。

次を保護します。

- データベースのパスワード。
- APIキー。
- SMTP認証情報。
- 決済・Webhookの秘密情報。
- バックアップ保存先の認証情報。
- パネル・管理者の認証情報。
- SSH秘密鍵。

担当者や外部委託先が離れたとき、または侵害が疑われるときは、認証情報を変更してください。

## コントロールパネルと管理画面 {#control-panels-and-admin-interfaces}

コントロールパネルは、強い権限を持つ管理アプリケーションです。

次を監査します。

- 現在のパネルのバージョン。
- パネルの管理者アカウント。
- 対応するパネルでは2FA。
- 公開されている管理ポート・ホスト名。
- 運用上可能な範囲での送信元IP制限。
- プラグイン・拡張機能の一覧。
- バックアップと復元の動作。
- パネルのログとログイン失敗。

パネルを入れるだけでVPSが安全になったり、マネージドになったりすると考えないでください。

パネル選びは、[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})をご覧ください。FASTPANELの導入については、[FASTPANEL対応VPS]({{< relref "fastpanel-vps-hosting.md" >}})で説明しています。

## アプリケーション・CMS・実行環境の更新 {#application-cms-and-runtime-updates}

OSにすべてのパッチを適用しても、アプリケーションに脆弱性が残る場合があります。

セキュリティの担当範囲に、次も含めます。

- PHP・Node・Pythonなどの実行環境。
- フレームワーク。
- WordPress本体。
- プラグイン・テーマ。
- WooCommerceと拡張機能。
- Webサーバー。
- 管理パネル。
- ライブラリと依存関係。

セキュリティ更新が提供されなくなった放置コンポーネントは削除してください。

WordPress固有の運用は、[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})をご覧ください。取引を扱うストアは、[WooCommerce向けVPS]({{< relref "vps-for-woocommerce.md" >}})で説明しています。

## HTTPSが保護するのは通信経路 {#https-protects-transport-not-the-whole-server}

ログインや機密データを扱う本番サイトにはHTTPSが必要です。公開サイト全般でも基本の対策です。

HTTPSはクライアントとサーバー間の通信中のデータを保護します。

次の問題を解決するものではありません。

- 脆弱なプラグイン。
- 弱いSSH設定。
- 公開されたデータベース。
- 漏えいしたAPIキー。
- 古いパッケージ。
- 安全でないファイル権限。
- バックアップの不足。

証明書の更新を確認し、有効期限切れや更新失敗を監視してください。

## DDoS対策とアプリケーションの保護は別 {#ddos-protection-is-not-application-security}

VDSinaは現在、Standard VPSで無料のDDoS対策を案内しています。

公開QAでは、無料サービスの対象を**L3-L4の回線・ネットワーク層への攻撃**とし、**SLAの対象外**と説明しています。

インフラ・ネットワーク層では有用ですが、次の代わりにはなりません。

- SSHの保護強化。
- ファイアウォール方針。
- Webアプリケーションのセキュリティ。
- アプリケーション層のレート制限。
- 必要に応じたWAF・ボット対策。
- パッチ適用。
- 障害対応。

ネットワーク層のDDoS軽減を、Webサイト全体のセキュリティサービスと捉えないでください。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">現在のVPSインフラを確認</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で注文されると当サイトが報酬を受け取る場合があります。事業者のDDoS対策と技術サポートは、ゲストOS・アプリケーションの保護強化や管理の代わりにはなりません。</small></p>

## バックアップもセキュリティ対策 {#backups-are-a-security-control}

侵害、ランサムウェア、更新失敗、誤削除から復旧できることも、セキュリティの一部です。

少なくとも、次を実施してください。

- 稼働中のVPSの外にコピーを保持します。
- 1つのスナップショット・イメージだけに頼らないでください。
- バックアップの認証情報を保護します。
- 可能な範囲で、アプリケーションからバックアップへアクセスできないようにします。
- バックアップジョブの失敗を監視します。
- 復元をテストします。
- 復元ポイント間で失う可能性のあるデータ量を把握します。

CISAは、重要データのオフライン・暗号化バックアップを保持し、障害復旧を想定して定期的に復元をテストすることを推奨しています。

RPO/RTO、保持期間、バックアップ構成の詳しい設計は、[VPSのバックアップ戦略]({{< relref "vps-backup-strategy.md" >}})をご覧ください。

## ログ・通知・監査記録 {#logs-alerts-and-audit-trail}

安全な設定でも、状態を確認しなければ失敗を見逃す場合があります。

少なくとも、次を確認します。

- SSH・認証の繰り返し失敗。
- 想定外の管理者・sudoユーザーの追加。
- パネルのログイン失敗。
- ファイアウォールの変更。
- 新たな待ち受けポート。
- サービスのクラッシュ・再起動。
- ディスク容量不足。
- アプリケーション・Webサーバーの5xx急増。
- バックアップの失敗。
- 証明書更新の失敗。
- 導入している場合はマルウェア・セキュリティツールの通知。

障害を調査できるだけの期間、ログを保持してください。

しきい値と通知の詳しい設計は、[VPSの監視]({{< relref "vps-monitoring.md" >}})をご覧ください。

## 侵害が疑われたら {#after-a-suspected-compromise}

特権・rootの侵害が疑われる場合、その場での「掃除」だけで安全になったと判断しないでください。

より安全な対応の流れは次のとおりです。

1. 影響を受けたVPS・ネットワーク経路を**隔離**します。
2. 可能な範囲で関連ログと証拠を保存します。
3. 漏えいした可能性のある認証情報・秘密情報を特定します。
4. クリーンで信頼できるシステムから認証情報を変更します。
5. 正常と確認できるアプリケーション・データの復元時点を決めます。
6. 必要に応じて、信頼できるOSと設定のソースからサーバーを再構築します。
7. 侵害された実行ファイルや設定を無条件に戻さず、検証済みデータを復元します。
8. 本番トラフィックを戻す前に、最初の侵入原因を調べます。

CISAのインシデント対応ガイドでも、隔離、証拠・ログの確認、検証済みバックアップからの復旧を重視しています。

業務上重要なシステムでは、インシデント対応・セキュリティの専門家を参加させてください。

## チェックリストを繰り返し確認する {#repeat-the-checklist}

セキュリティは初期構築時だけの作業ではありません。

決めた周期で次を再確認します。

- 管理ユーザーとSSH鍵。
- sudo権限。
- 開放・待ち受けポート。
- ファイアウォールルール。
- サポート終了のパッケージ・OSバージョン。
- 未適用のセキュリティ更新。
- パネル・CMS・プラグインのバージョン。
- バックアップの成功と復元テスト。
- 証明書の期限と更新。
- ログと通知。
- 未使用のアカウント・サービス。
- 公開された秘密情報。
- インシデント時の連絡先。

大きな移行、パネル変更、新サービスの追加、構成変更の後にも再確認してください。

## 本番環境のセキュリティチェックリスト {#production-security-checklist}

| 対策 | 合格条件 |
|---|---|
| 復旧アクセス | 事業者のコンソール・復旧経路が動作する |
| 管理ログイン | 個人用の非root管理者で鍵ログインを確認した |
| SSH方針 | 安全な代替経路を確認後、root・パスワード方針を明確に設定した |
| サービス | 待ち受けポートを把握し、必要性を説明できる |
| ファイアウォール | 原則拒否・最小限の公開とし、必要な管理・Webアクセスを確認した |
| 内部サービス | 明確な理由なくDB・キャッシュ・アプリ用ポートを公開していない |
| パッチ | OS・アプリ更新の担当者と、サービス・OS再起動の手順がある |
| 最小権限 | アプリ・DB・ユーザーに必要な権限だけを与えた |
| 秘密情報 | 公開せず、Webや広い権限から読み取れない |
| パネル・管理画面 | 更新済みで、管理アクセス・2FA・制限を確認した |
| TLS | 有効なHTTPSと証明書更新の経路がある |
| 総当たり攻撃対策 | 有用な場合に多層防御として利用している |
| バックアップ | 独立コピーがあり、復元をテストした |
| ログ | 認証・管理・サービス・バックアップの失敗を把握できる |
| DDoS | 事業者・ネットワーク対策の範囲を理解している |
| インシデント対応 | 担当者、隔離、クリーンな復旧の手順がある |
| 定期監査 | 次の確認日と手順が決まっている |

## 技術資料 {#technical-references}

- Ubuntu Server — OpenSSH
- Ubuntu Server — ファイアウォール・UFW
- Ubuntu Server — 自動更新
- CISA — StopRansomwareガイド
- VDSina Standard VPS
- VDSina QA — DDoS対策の範囲

## よくある質問 {#faq}

### 新しいVPSでは何から保護すべきですか？ {#what-should-i-secure-first-on-a-new-vps}

コンソール・復旧アクセスを確保し、個人用の非root管理ユーザーでSSH鍵ログインを確認します。待ち受けサービスを把握してから、SSHとファイアウォールを制限します。アクセス確認前に、締め出しにつながる変更をまとめて行わないでください。

### SSHのパスワードログインを無効にすべきですか？ {#should-i-disable-ssh-password-login}

一般的なVPS管理では鍵認証のほうが強固ですが、先に鍵ログインと復旧コンソールを確認してください。唯一動作するアクセス経路を無効にしないでください。

### SSHのポートを変えるべきですか？ {#should-i-change-the-ssh-port}

スキャンやログのノイズを減らせる場合がありますが、主要な防御ではありません。強固な認証、最小権限、ファイアウォール方針、パッチのほうが重要です。

### Fail2banは必要ですか？ {#do-i-need-fail2ban}

必須とは限りませんが、繰り返しの不正ログインに対する多層防御として役立ちます。SSH鍵、パッチ、適切な公開範囲の代わりにはなりません。

### VPSではどのポートを開くべきですか？ {#which-ports-should-be-open-on-a-vps}

構成上必要なポートだけです。公開Webサーバーでは通常HTTP/HTTPSと、制御された管理経路が必要です。DBと内部アプリケーションサービスは原則非公開にします。

### ファイアウォールは脆弱なアプリケーションを保護できますか？ {#does-a-firewall-protect-a-vulnerable-application}

いいえ。ファイアウォールが制限するのはネットワークの公開範囲です。公開Webアプリケーションには、安全なコード、サポート中の依存関係、更新、アプリケーション側の対策が引き続き必要です。

### セキュリティ自動更新だけで十分ですか？ {#are-automatic-security-updates-enough}

いいえ。対応するOSパッケージには役立ちますが、外部アプリや依存関係は別の更新が必要な場合があります。サービス・OS再起動の運用も必要です。

### HTTPSだけでVPSを保護できますか？ {#is-https-enough-to-secure-a-vps}

いいえ。HTTPSは通信経路を保護します。弱いSSH、公開DB、脆弱なプラグイン、古いパッケージ、秘密情報の漏えい、バックアップ不足は解決しません。

### VDSinaのDDoS対策だけでサイトを保護できますか？ {#is-vdsina-ddos-protection-enough-to-secure-the-website}

いいえ。現在、無料DDoS対策が案内されていますが、公開QAではL3-L4が対象でSLAはないと説明されています。ゲストOS、アクセス、アプリケーション、復旧の対策が別途必要です。

### VPSの侵害が疑われたらどうすべきですか？ {#what-should-i-do-if-i-suspect-the-vps-was-compromised}

隔離し、関連する証拠・ログを保存し、クリーンなシステムから漏えいした認証情報を変更します。特権侵害が疑われる場合は、信頼できるソースから再構築し、検証済みバックアップを使う方法を優先します。重要システムではインシデント対応の専門家に参加してもらってください。
