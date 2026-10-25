---
title: "VPSでWebサイトを公開する方法"
description: "VPSでWebサイトを公開する方法。構築方式を選び、初回アクセスを保護し、必要な環境、ドメイン、HTTPSを設定。再起動からの復旧と本番運用の準備を確認します。"
image: "images/home/vps-for-website-hero.webp"
slug: "vpsでwebサイトを公開する方法"
---

VPSでWebサイトを公開する方法は、アプリの種類で変わります。静的サイトはWebサーバーとDNS、WordPressなどのPHP CMSはさらにPHPとDBが必要です。Node.js・Pythonアプリは通常リバースプロキシの背後で動かします。クリーンなVPSへ手動で構築するか、パネルでブラウザーから管理できます。

このガイドは、**新しいVPSからWebサイト公開まで**を説明します。更新中の本番データを持つ既存サイトを移す場合は、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})で切り替えと切り戻しの手順を確認してください。

VPS選び全体については、[Webサイト向けVPS]({{< relref "_index.md" >}})をご覧ください。

[構築の順序](#quick-deployment-sequence) · [方式を選ぶ](#choose-manual-panel-or-managed) · [構築方式チェック](#deployment-path-checker) · [手動構築](#manual--no-control-panel-path) · [DNS](#point-the-domain-to-the-vps) · [本番前チェック](#production-acceptance-checklist) · [よくある質問](#faq)

## 公開までの構築手順 {#quick-deployment-sequence}

初回公開は、次の順序で進めます。

1. **VPSと必要スペックを選ぶ。**
2. **手動・パネル・管理サービスの方式を選ぶ。**
3. **クリーンなOS、または現在提供されているパネルイメージを導入する。**
4. **初回アクセスを保護し、非rootの管理経路を作る。**
5. **OSを更新する。**
6. **アプリが必要とするWeb環境だけを導入する。**
7. **可能な範囲で、公開DNSを切り替える前にサイト・アプリを設定する。**
8. **ファイル・コードを配置し、所有権、秘密情報、DBアクセスを設定する。**
9. **SSHと必要なHTTP/HTTPSを維持しながら、ファイアウォールを制限する。**
10. **公開DNSの変更前に移行先をテストする。**
11. **ドメインをVPSへ向ける。**
12. **ホスト名がサーバーへ到達するようになったらHTTPSを有効にする。**
13. **cron・ワーカー、ログ、バックアップ、外部監視を確認する。**
14. **一度再起動し、必要なサービスがすべて自動復帰するか確認する。**
15. **ここまで確認して、本番公開の準備完了とする。**

一般的なVPSガイドに載っているという理由だけで、PHP、MySQL、メール、パネルを入れないでください。サイトに実際に必要な構成要素を導入します。

## 手動・パネル・管理サービスを選ぶ {#choose-manual-panel-or-managed}

運用には3つの異なる方式があります。

### 手動管理・パネルなし {#manual--no-control-panel}

クリーンなLinux VPSを選び、SSHで構成を管理します。

次の場合に適しています。

- アプリの構成を理解している。
- 稼働するサービスを最小限にしたい。
- Nginx・Apache・実行環境の独自設定が必要。
- スクリプト、Git、Infrastructure as Codeを使う。
- 従来型のホスティングアカウント画面が不要。

**コントロールパネルなしのVPS**でサイトを公開する場合も、このページの手動構築手順を利用できます。

### コントロールパネル {#control-panel}

サイト、ドメイン、PHP、DB、メール、ユーザーをブラウザーで管理することで、繰り返し作業を十分減らせる場合に使います。

[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})をご覧ください。FASTPANELを選んでいる場合は、[FASTPANEL対応VPS]({{< relref "fastpanel-vps-hosting.md" >}})が適しています。

### 管理サービスの利用 {#managed-administration}

パネルと管理サービスは別です。パッチ、セキュリティ、バックアップ、監視、障害対応の担当者がいなければ、公開前に決めてください。

[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})をご覧ください。

## 構築方式チェック {#deployment-path-checker}

調べるべき構成を見つけるツールです。アプリの公式ドキュメントの代わりにはなりません。

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="deployment-path-checker-form">
  <div class="mb-6">
    <label for="deploy-type" class="form-label">Webサイト・アプリの種類</label>
    <select id="deploy-type" class="form-input">
      <option value="static">静的HTML・生成済みの静的サイト</option>
      <option value="php">WordPress・PHP CMS</option>
      <option value="app">Node.js・Python・独自アプリ</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="deploy-panel" class="form-label">ホスティング用パネルを使いたい？</label>
    <select id="deploy-panel" class="form-input"><option value="no">いいえ・手動管理</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-db" class="form-label">アプリにローカルDBが必要？</label>
    <select id="deploy-db" class="form-input"><option value="no">いいえ</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-mail" class="form-label">同じVPSでメールボックスを運用する？</label>
    <select id="deploy-mail" class="form-input"><option value="no">いいえ・外部メール</option><option value="yes">はい</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-sites" class="form-label">稼働するWebサイト数</label>
    <select id="deploy-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">構築方式を確認</button>
</form>
<p id="deployment-path-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">処理内容と希望する管理方式を選んでください。</p>
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
      result = "コントロールパネル方式：最終的なOSイメージを選ぶ前にパネルを決めます。OS互換性、追加負荷、ユーザー・サイトの分離、メール・DNS、バックアップ、管理責任を確認してください。";
    } else if (type === "static" && !db && !mail) {
      result = "静的サイトの手動構築：クリーンなLinux＋SSH＋NginxまたはApache＋サイトファイル＋DNS＋HTTPS。実際に必要でなければ、PHPやDBをインストールしないでください。";
    } else if (type === "php") {
      result = "PHP・WORDPRESSの手動構築：Linux＋SSH＋Nginx/Apache＋PHP-FPM＋必要に応じたDB＋DNS＋HTTPS。PHPワーカーとDB用のRAMを見積もってください。";
    } else if (type === "app") {
      result = "アプリ＋リバースプロキシ方式：アプリを専用の非rootサービス・プロセス管理下で、通常はlocalhostにバインドして実行します。前段にNginx/Apacheを置き、公開ホスト名とHTTPSを処理します。";
    } else {
      result = "独自アプリの手動構築：公式の実行環境要件から始め、必要なサービスだけを導入してください。";
    }

    if (sites === "many") {
      result += " 6サイト以上では、サイト別のユーザー・権限を明確にし、合計負荷を計画してください。";
    }
    if (mail) {
      result += " 同じVPSでメールを運用すると、SMTP/IMAP、DNSと送信元評価、容量、バックアップ、セキュリティの作業が増えます。外部の管理型メールが簡単でないか再検討してください。";
    }

    document.getElementById("deployment-path-result").textContent = result;
  });
});
</script>

## 事前に用意するもの {#prerequisites}

サーバーを操作する前に、次を用意します。

- 処理負荷に合うスペックのVPS。
- サーバーのIPアドレス。
- SSH認証情報、または鍵アクセス。
- 動作する事業者コンソール・VNC・復旧経路。
- 登録済みドメインとDNS操作権限。
- サイトファイル、またはアプリのリポジトリー。
- 必要な実行環境のバージョン。
- DB要件。
- 秘密情報・環境変数の管理計画。
- バックアップの保存先。
- 外部からサイトの稼働を確認する方法。

必要リソースが不明なら、導入前に[VPSのスペックの選び方]({{< relref "vps-sizing-for-website.md" >}})を確認してください。

現在のVDSina Standard VPSページでは、パネルなしのOSテンプレートとしてUbuntu 26.04/24.04/22.04/20.04、Debian 13/12/11/10、AlmaLinux、Rocky、CentOS、Oracle Linux、ArchLinuxが掲載されています。このガイドでは、Webサーバーの公式資料とパッケージ操作を追いやすいUbuntu・Debian系の例を使います。ほかの対応Linuxにも考え方は適用できますが、パッケージ・サービスのコマンドは変わります。

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Webサイト用のVPSを選ぶ</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があり、この提携リンク経由で注文されると当サイトが報酬を受け取る場合があります。スペックと運用方式は、報酬ではなく実際の処理負荷から選んでください。</small></p>

## OSを選ぶ {#choose-the-operating-system}

手動でWebサーバーを構築するなら、次のOSを選びます。

- アプリ・実行環境が対応している。
- 現在も保守されている。
- 管理者が理解している。
- Web環境の新しいパッケージ・資料がある。
- 後でパネルを使う場合は、その要件に合う。

最新という理由だけで選ばないでください。アプリ互換性と管理者の習熟のほうが重要です。

Linuxの分かりやすい例として、Ubuntu 24.04 LTSやDebian 12を資料上の対象にできます。アプリ提供元が別のサポート中ディストリビューションを指定する場合は、その要件に従ってください。

## 初回SSHアクセスを保護する {#secure-first-ssh-access}

新VPSでは管理権限を得られますが、本番作業を常にrootで行うべきではありません。

安全な初回アクセスの流れは次のとおりです。

1. 事業者が提供した認証情報・鍵で接続する。
2. 意図して作成したサーバー・IPであることを確認する。
3. 事業者のコンソール・VNC・復旧経路を使える状態に保つ。
4. 個人を識別できる管理ユーザーを作る。
5. 必要なsudo・管理者権限だけを与える。
6. 可能な範囲でSSH鍵認証を設定する。
7. 元のアクセス方法を無効化・制限する**前に**、別セッションで新しいログインを確認する。

Ubuntu・Debianでの例：

```bash
ssh root@SERVER_IP
adduser deploy
usermod -aG sudo deploy
```

保護強化のつもりで、唯一動作する管理経路から締め出されないようにしてください。

SSH・ファイアウォールの詳しい強化は、[VPSのセキュリティチェックリスト]({{< relref "vps-security-checklist.md" >}})で扱います。このガイドでは公開に必要な最低限を説明します。

## 環境構築の前にサーバーを更新する {#update-the-server-before-installing-the-stack}

Ubuntu・Debianの場合：

```bash
sudo apt update
sudo apt upgrade -y
```

更新で必要なら再起動し、再接続できることを確認します。

セキュリティ更新をサイト公開後まで延期しないでください。

## 手動構築・コントロールパネルなしの手順 {#manual--no-control-panel-path}

手動構築のVPSには、アプリが必要とするサービスだけを入れます。

一般的な構成は次のとおりです。

### 静的Webサイト {#static-website}

必要なもの：

- NginxまたはApache。
- サイトのファイル。
- DNS。
- HTTPS。

必ずしも必要でないもの：

- PHP。
- MySQL・MariaDB・PostgreSQL。
- ローカルのメールサーバー。

### PHP・WordPressサイト {#php--wordpress-website}

通常必要なもの：

- NginxまたはApache。
- PHP-FPM・PHPモジュール。
- データベース。
- サイトファイル・アップロード。
- DNS。
- HTTPS。

WordPressのリソース特性は、[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})をご覧ください。

### Node.js・Python・独自アプリ {#nodejs--python--custom-application}

一般的な構成：

- アプリの実行環境。
- 専用の非rootアプリユーザー。
- プロセス管理・systemdサービス。
- 可能な範囲でlocalhost・非公開ソケットにバインドしたアプリ。
- Nginx/Apacheのリバースプロキシ。
- 必要な場合だけDB。
- DNS。
- HTTPS。

開発用サーバーをそのままインターネットへ公開し、本番構成として使わないでください。

## Webサーバーをインストールする {#install-the-web-server}

Ubuntuの現在のサーバードキュメントでは、NginxとApacheの両方を扱っています。どちらかが常に優れているわけではありません。

Nginxの例：

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

ネットワーク・ファイアウォールがHTTPを許可していれば、この時点でサーバーIPからNginxの初期ページが返ります。

アプリ、チーム、既存設定にApacheがより合う場合は、そちらを使ってください。

## Webサイトのホスト名を設定する {#configure-the-website-hostname}

DNSとWebサーバーの設定は、両方が必要です。

DNSでホスト名をVPSへ向け、**さらに**Webサーバーでそのホスト名に応答するサイトを指定します。

Nginxではドメイン用のサーバーブロックを作ります。概念的には次のようになります。

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

Ubuntu・Debianでは、サイト別設定を一般に次へ置きます。

- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

変更後：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

再読み込みの前に、必ず設定構文をテストしてください。

リバースプロキシ型のアプリでは、サーバーブロックからローカルのアプリポート・ソケットへ転送します。

## ファイル・アプリコードを配置する {#deploy-files-or-application-code}

繰り返し実行できるデプロイ方法を選びます。

### SFTP/SCP {#sftpscp}

次に適しています。

- 小規模サイト。
- 頻度の低い手動デプロイ。
- 初めての単純なプロジェクト。

本番ディレクトリーとソースリポジトリーの内容がずれやすい点に注意が必要です。

### SSH経由のrsync {#rsync-over-ssh}

再現可能なファイル同期と、効率的な差分更新に役立ちます。

### Gitを使うデプロイ {#git-based-deployment}

本番リリースをリポジトリーのコミットに対応させたい場合に役立ちます。

### CI/CD {#cicd}

ビルド・テスト・公開の自動化に見合う頻度でデプロイする場合に役立ちます。

どの方法でも、次を守ります。

- 作業にroot権限が必要な場合を除き、rootでデプロイしない。
- アプリのファイルは、適切なデプロイ・アプリユーザーが所有する。
- Webサーバーには必要なアクセスだけを与える。
- 秘密情報は公開ドキュメントルートの外へ置く。
- 誰でも書き込める権限を近道として使わない。

## PHP・WordPressの構築 {#php--wordpress-path}

Ubuntu・DebianのPHPサイトでは、現在サポートされるPHP-FPMパッケージと、アプリに必要な拡張を導入します。

一般的な構成：

**ブラウザー → Nginx/Apache → PHP-FPM → データベース**

別CMSの拡張一覧を無条件にコピーせず、実際に必要なものを導入してください。

WordPressでは、次を行います。

- DBと専用DBユーザーを作る。
- 実測した必要量から、PHPのアップロード・メモリ・実行時間上限を設定する。
- `wp-config.php`の秘密情報を保護する。
- サイトのホスト名を設定する。
- HTTPSを有効にする。
- wp-cron・バックグラウンド処理を検証する。
- 処理内容に合うキャッシュを追加する。

スペックと性能については、[WordPress向けVPS]({{< relref "vps-for-wordpress.md" >}})をご覧ください。

## Node.js・Python・独自アプリの構築 {#nodejs--python--custom-app-path}

ターミナルで開発用コマンドを手動実行しただけで、本番運用としないでください。

次のように考えます。

- 専用のアプリユーザー。
- 権限を制限した環境変数・設定ファイル。
- systemd、または適切な本番用プロセス管理。
- 障害・OS再起動後の自動起動。
- ローカル・非公開のアプリ待ち受け。
- Nginx/Apacheのリバースプロキシ。
- アプリケーションログ。
- ヘルスチェック。

一般的な流れ：

**ブラウザー → HTTPS/Nginx → 127.0.0.1:PORTのアプリ → DB・外部サービス**

フレームワーク自身の本番公開ガイドを確認してください。

## DBは必要な場合だけ導入する {#database-install-only-when-required}

静的サイトにDBは不要です。

動的アプリで必要な場合は、次を行います。

- 対応するDBエンジンを導入する。
- 専用DBを作る。
- アプリ専用ユーザーを作る。
- 必要な権限だけを与える。
- 認証情報をWebルートの外へ置く。
- 安全に設計した構成で明確に必要な場合を除き、DBポートを公開しない。
- DBをバックアップと監視の計画に含める。

Webサーバーがほぼアイドルでも、DB処理がVPSのボトルネックになる場合があります。

## ファイル所有権・権限・秘密情報 {#file-ownership-permissions-and-secrets}

よくある2つの間違いを避けます。

1. サイトをrootで動かす。
2. 権限エラーを直すために、アプリのディレクトリーを誰でも書き込める状態にする。

次のように設定します。

- デプロイ・アプリユーザーを使う。
- どのプロセスが読み取り・書き込みを必要とするか理解する。
- アップロード・キャッシュ先に必要な書き込み権限だけを与える。
- 環境変数ファイルと認証情報を保護する。
- 本番の秘密情報をGitへコミットしない。
- 秘密鍵を公開ドキュメントルートの外へ置く。

正確な所有権は、アプリとWebサーバーの方式で変わります。万能な`chmod 777`の手順をコピーせず、アプリのドキュメントに従ってください。

## 公開DNSを変える前にテストする {#test-before-public-dns}

DNSを変えた瞬間が、アプリの最初の実動テストにならないようにします。

公開切り替え前に、可能な方法で新サーバーを検証します。

- 単純な初期・静的確認ではサーバーIPへアクセスする。
- ローカルのhostsを上書きし、自分のPCだけで`example.com`を新VPSへ解決させる。
- 意図せず検索へ登録されないようにした、非公開・テスト用ホスト名を使う。
- 本番と同じNginx/Apacheのホスト名設定を通してアプリをテストする。

ホームページ以外も確認します。

- 重要な内部ページ。
- ログイン・管理画面。
- フォーム。
- アップロード。
- 静的アセット。
- データベースの読み書き。
- アプリ・APIエンドポイント。
- リダイレクト。
- ログ。

アプリは生のIPと実際のホスト名で動作が異なる場合が多いため、hostsによるテストが特に役立ちます。

既存の本番サイトなら、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})のより厳密な切り替え手順を使ってください。

## ドメインをVPSへ向ける {#point-the-domain-to-the-vps}

DNS事業者側で、このサーバーへ到達させるレコードを設定します。

一般的なIPv4設定：

| 名前 | 種類 | 値 |
|---|---|---|
| `@` | A | VPSのIPv4アドレス |
| `www` | CNAME | ルートドメイン |

`www`にAレコードを使う方法もあります。

AAAAは、VPSでIPv6を実際に設定し、到達可能な場合だけ追加します。誤ったAAAAがあると、IPv4が動いていても一部利用者が接続できない場合があります。

DNSだけではサイトは動きません。Nginx/Apache側にも一致するホスト名の設定が必要です。

既存の本番サイトを移す場合、DNS切り替えと最終書き込みは、[WebサイトのVPS移行]({{< relref "website-migration-to-vps.md" >}})で扱います。

## DNSが解決したらHTTPSを追加する {#add-https-after-dns-resolves}

公開ホスト名が検証要求に応答するサーバーへ解決されてから、信頼された証明書を取得します。使うHTTP/HTTPS検証経路が、ファイアウォールと事業者のネットワークで許可されていることを確認してください。

Nginx/Apacheでは、CertbotなどのACMEクライアントでLet's Encrypt証明書を取得・更新できます。古いパッケージコマンドを無条件にコピーせず、最新のCertbot・OS手順に従ってください。

次を確認します。

- 使用するルートドメインと`www`が証明書に含まれる。
- HTTPからHTTPSへ意図どおり転送される。
- 証明書の更新が自動化されている。
- 更新時の通信がファイアウォール・CDNを通る。
- アプリが正しいHTTPS URLを生成する。

証明書の経路が動くと確認する前に、HTTPSへの転送を有効にしないでください。

## ファイアウォールを設定する {#configure-the-firewall}

ルールを変える間も、管理アクセスを維持します。

基本的な公開サイトでは、一般に次が必要です。

- 必要な管理元・経路からのSSH。
- HTTP・ACME・転送用のTCP 80。
- HTTPS用のTCP 443。

MySQL/PostgreSQL、Redis、内部アプリがローカルで待ち受けているという理由だけで、ポートを公開しないでください。

UFWを使うサーバーでは、厳しいルールを有効にする**前に**必要なSSH経路を許可します。

詳しいファイアウォールと保護強化は、[VPSのセキュリティチェックリスト]({{< relref "vps-security-checklist.md" >}})をご覧ください。

## cron・キュー・ワーカー {#cron-jobs-queues-and-workers}

Webリクエストの経路しか設定しなかったために、公開後に動的サイトで問題が起きることがあります。

次を洗い出します。

- cronジョブ。
- キューワーカー。
- スケジュール済みアクション。
- インポート・エクスポート。
- メール送信処理。
- キャッシュのウォームアップ。
- バックグラウンド処理。

次のように設定します。

- 正しい非rootユーザーで実行する。
- 必要なときに自動起動する。
- 場所が分かるログへ出力する。
- CPU・RAMを使い切るような重複を避ける。
- サーバー再起動後も動作する。

## ログと基本的な状態把握 {#logs-and-basic-observability}

本番アクセスを受ける前に、サイトが壊れたときの確認先を把握します。

少なくとも、次の場所を確認してください。

- Nginx/Apacheのアクセスログ。
- Nginx/Apacheのエラーログ。
- アプリケーションログ。
- PHP-FPM・実行環境のログ。
- DBのログ・状態。
- システムジャーナル。
- ディスク使用量。
- メモリ・CPUの逼迫。

誰もVPSへログインしていなくても障害が分かるように、外部HTTP(S)稼働監視を追加します。

詳しいしきい値・通知設計は、[VPSの監視]({{< relref "vps-monitoring.md" >}})をご覧ください。

## 再起動後の動作確認 {#reboot-validation}

初めて構築したVPSが、最初の再起動までは動いていたというケースは少なくありません。

準備完了とする前に、次を実行します。

```bash
sudo reboot
```

再起動後に、次を確認します。

- SSHアクセス。
- Nginx・Apache。
- PHP-FPMまたはアプリサービス。
- データベース。
- cron・キューワーカー。
- HTTPS。
- サイトのページ・フォーム。
- 監視。
- バックアップのスケジュール。

誰かが手動でコマンドを実行しないとアプリが戻らないなら、構築は未完了です。

## 手動・パネルなしの運用が適さない場合 {#when-manual--no-panel-hosting-is-the-wrong-fit}

次の場合は、パネルや管理サービスを検討してください。

- SSHとコマンドラインでの復旧に慣れた人がいない。
- OS・セキュリティ更新の担当者がいない。
- Webサーバー・実行環境・DBの障害を診断できる人がいない。
- バックアップを作っていても、復元できる人がいない。
- 業務上重要な停止に対応する担当者がいない。
- チームがサーバー設定よりも、画面でメール・ユーザー・ドメインを管理したい。
- アプリの構成に、管理型プラットフォームのほうが合う。

手動VPSはパネルの追加負荷を減らし、制御の自由度を高められますが、運用責任が減るわけではありません。

パネル選びは[コントロールパネル付きVPS]({{< relref "vps-with-control-panel.md" >}})、運用担当の不足は[マネージドVPSとアンマネージドVPSの違い]({{< relref "managed-vs-unmanaged-vps.md" >}})をご覧ください。

## 本番公開の受け入れチェックリスト {#production-acceptance-checklist}

| 確認項目 | 合格の条件 |
|---|---|
| サーバーアクセス | 個人用管理者でログインでき、復旧コンソールも使える |
| 更新 | 現在のセキュリティ・システム更新を適用済み |
| Webサーバー | 自動起動し、設定テストに合格する |
| サイトのホスト名 | ルート・`www`の動作が意図どおり |
| DNS | A・AAAA・CNAMEが意図するサーバー・経路へ解決される |
| HTTPS | 信頼された証明書、正しい名前、把握済みの更新経路がある |
| アプリ | 代表ページ、ログイン、フォーム、アップロードが動く |
| データベース | アプリユーザーが動作し、DBポートを意図せず公開していない |
| ファイル | 所有権が正しく、`777`で回避していない |
| 定期処理 | cron・ワーカーが起動し、正しくログを残す |
| 再起動 | 必要なサービスが自動復帰する |
| ログ | Web・アプリ・システムの失敗の確認先を担当者が把握している |
| バックアップ | 必要なファイル・DBを含み、復元手順がある |
| 監視 | 外部サイト確認と基本的なリソース監視がある |
| 処理能力 | 実際の負荷でCPU・RAM・ディスクを確認した |

ホームページがHTTP 200を返すだけでは、本番準備が整ったとはいえません。

## バックアップと監視へ引き継ぐ {#backups-and-monitoring-handoff}

このページでは、運用へ引き継ぐ最低限を示します。

サイトを本格的に使う前に、次を行います。

- バックアップを定期設定する。
- 独立したサーバー外コピーを保持する。
- 復旧に必要なDB、設定、秘密情報を含める。
- 復元できることを検証する。
- サイトの稼働を監視する。
- ディスクの増加を監視する。
- CPU・RAM・DBの逼迫を確認する。
- 証明書更新を確認する。

詳しい復旧設計は[VPSのバックアップ戦略]({{< relref "vps-backup-strategy.md" >}})、しきい値と通知設計は[VPSの監視]({{< relref "vps-monitoring.md" >}})をご覧ください。

## 複数のWebサイト {#multiple-websites}

複数サイトでは、次を行います。

- ホスト名ごとにサーバーブロック・仮想ホストを分ける。
- ドキュメントルートを分ける。
- アプリ・DBの認証情報を分ける。
- 信頼関係の設計で必要ならOSユーザーを分ける。
- 1サイトのcron・インポート・バックアップで他サイトを圧迫しない。
- 合計ピーク負荷を考慮する。
- 全サイトが1台のVPSの障害範囲を共有すると理解する。

処理能力と分離の計画は、[複数サイト向けVPS]({{< relref "vps-for-multiple-websites.md" >}})をご覧ください。

## 技術資料 {#technical-references}

- Ubuntu Server：Nginxのインストール
- Ubuntu Server：Nginxの設定
- Ubuntu Server：Webサービス
- VDSina Standard VPS — 現在のパネルなしOSテンプレート

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">サイトに合うVPSを選ぶ</a>
</p>
<p><small>広告・提携について：編集者はVDSinaと業務上の関係があります。提携リンクにはsponsored属性を付けています。注文前に、現在のVPS料金、OSの提供状況、事業者の条件を確認してください。</small></p>

## よくある質問 {#faq}

### パネルなしのVPSでWebサイトを公開できますか？ {#can-i-host-a-website-on-a-vps-without-a-control-panel}

はい。クリーンなLinux VPSにSSHで接続し、アプリに必要なWebサーバー、実行環境、DBを構築できます。パネルなしの手順も、このガイドで説明しています。

### VPSでサイトを公開するにはNginxが必要ですか？ {#do-i-need-nginx-to-host-a-website-on-vps}

必須ではありません。NginxとApacheはどちらも一般的です。アプリ、設定、管理者の経験に合うWebサーバーを使ってください。

### すべてのVPSサイトにDBが必要ですか？ {#does-every-vps-website-need-a-database}

いいえ。静的サイトには不要です。アプリが必要とする場合だけ、MySQL/MariaDB/PostgreSQLを導入してください。

### rootでサイトを運用すべきですか？ {#should-i-use-root-to-host-the-website}

いいえ。rootは管理用です。サイトの実行・配置には、必要な権限だけを持つ適切な非rootユーザーとサービスを使います。

### どのような場合にパネルを使うべきですか？ {#when-should-i-use-a-control-panel}

サイト、ドメイン、PHP、DB、ユーザー、メール、バックアップのブラウザー管理で、追加負荷と制約に見合うだけ繰り返し作業を減らせる場合です。

### cPanelなしのVPSでWordPressを運用できますか？ {#can-i-host-wordpress-on-a-vps-without-cpanel}

はい。互換性のあるWebサーバー、PHP、DB、WordPressファイル、正しい権限、DNS、HTTPSが必要です。パネルは任意です。

### いつDNSをVPSへ向けるべきですか？ {#when-should-i-point-dns-to-the-vps}

新規サイトなら、実際のホスト名へ応答できる準備が整ってからです。既存の本番サイトなら、先にテストし、計画した移行・切り替え手順を使います。

### ドメインはVPSを向いているのに別サイトが出るのはなぜですか？ {#why-does-my-domain-point-to-the-vps-but-show-the-wrong-site}

DNSはホスト名をサーバーIPへ向けるだけです。Nginx/Apacheにも、そのホスト名に一致するサーバーブロック・仮想ホストが必要です。

### HTTPSはいつ有効にすべきですか？ {#when-should-i-enable-https}

公開ホスト名がサーバーへ解決され、検証経路が動いてからです。証明書を発行し、ルート・`www`の対象範囲を確認して、意図したHTTPからHTTPSへの転送を設定します。

### VPSの再起動後に何を確認すべきですか？ {#what-should-i-check-after-rebooting-the-vps}

Webサーバー、アプリサービス・PHP-FPM、DB、ワーカー、HTTPS、監視、サイトが、手動操作なしに復帰することを確認してください。
