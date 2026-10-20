---
title: "웹사이트 VPS 이전"
slug: "웹사이트-vps-이전"
description: "웹사이트 VPS 이전 가이드. 기존 환경을 조사하고 새 서버를 테스트한 뒤 데이터 쓰기와 최종 동기화를 관리하고, DNS·메일·SEO를 보호하면서 롤백할 수 있게 이전하세요."
image: "images/home/vps-for-website-hero.webp"
---

웹사이트를 VPS로 이전할 때 가장 안전한 방법은 **기존 호스팅이 트래픽을 처리하는 동안 새 서버를 구축하고 테스트하는 것**입니다. 현재 구성을 조사하고, 새 VPS의 사양을 정한 뒤 웹사이트를 복사해 검증하세요. 마지막 데이터 변경을 통제한 뒤 DNS를 전환하고, 기존 서버를 종료할 수 있을 때까지 두 환경을 모니터링해야 합니다.

이 가이드는 **도메인과 공개 URL 구조를 유지하는 이전**을 전제로 합니다. 도메인이나 경로까지 바꾼다면 기존 URL과 새 URL의 매핑 및 영구 리디렉션을 별도의 작업으로 계획해야 합니다.

VPS 선택 자체를 검토하는 단계라면 [웹사이트용 VPS 호스팅]({{< relref "_index.md" >}}) 가이드를 먼저 확인하세요.

[이전 순서](#quick-migration-plan) · [전환 전 점검](#migration-cutover-preflight) · [최종 동기화](#control-new-writes-and-the-final-sync) · [DNS 전환](#switch-dns-deliberately) · [SEO 점검](#preserve-seo-when-urls-stay-the-same) · [자주 묻는 질문](#faq)

## 웹사이트 이전의 핵심 절차 {#quick-migration-plan}

통제 가능한 이전은 다음 순서로 진행합니다.

1. **기존 환경 조사.** 애플리케이션, 실행 환경, 데이터베이스, 파일, DNS, 메일, cron 작업, 워커, 웹훅과 외부 서비스 의존성을 기록합니다.
2. **새 서버 자원 산정.** 실제 부하와 이전 작업에 필요한 여유 공간을 고려해 CPU·RAM·디스크를 선택합니다.
3. **복원 가능한 백업 확보.** 기존 서버 외부에 사본을 보관하고 필요한 데이터베이스와 파일이 포함되어 있는지 검증합니다.
4. **새 VPS 병렬 구축.** 트래픽을 옮기기 전에 웹 서버나 관리 패널을 설치하고 애플리케이션 요구사항을 맞춥니다.
5. **전체 데이터의 첫 복사.** 기존 사이트가 운영되는 동안 파일을 전송하고 데이터베이스를 가져옵니다.
6. **비공개 테스트.** hosts 파일 설정, 관리되는 미리보기 호스트 이름 등으로 DNS 변경 전에 실제 새 환경을 테스트합니다.
7. **최종 데이터 쓰기 관리.** 쇼핑몰, 회원 사이트, 양식 등 데이터가 바뀌는 서비스는 잠시 쓰기를 중단하거나 애플리케이션에 맞는 최종 변경분 동기화를 계획합니다.
8. **마지막에 DNS 전환.** 실제로 이전할 레코드만 변경하고 메일·도메인 인증 레코드는 보존합니다.
9. **두 서버 동시 모니터링.** 트래픽, 오류, 양식, 주문, cron, 웹훅, 메일, HTTPS 및 검색엔진 크롤링을 확인합니다.
10. **검수 후 기존 호스팅 종료.** 롤백할 수 있도록 정해 둔 기간에는 기존 환경을 유지합니다.

모든 사이트에서 무중단 이전을 보장할 수는 없습니다. 목표는 불필요한 데이터 손실 없이 중단 시간을 현실적으로 최소화하는 **통제된 전환**입니다.

## 실제로 어떤 시스템을 이전하는지 정의하기 {#define-what-is-actually-moving}

'웹사이트 이전'에는 서로 다른 여러 시스템이 포함될 수 있습니다. 복사 작업을 시작하기 전에 범위를 확정하세요.

| 구성 요소 | 이전 전에 확인할 사항 |
|---|---|
| 웹사이트·애플리케이션 | CMS·프레임워크, 문서 루트, 업로드 파일, 숨김 파일, 캐시, 쓰기 가능한 디렉터리 |
| 실행 환경 | PHP·Node·Python 버전, 확장 모듈, 웹 서버, 프로세스 관리자 |
| 데이터베이스 | 엔진·버전, 크기, 사용자·권한, 문자 집합, 예정된 유지보수 |
| DNS | 서비스 제공업체, A·AAAA·CNAME 레코드, www·루트 도메인 동작, TTL, 인증 레코드 |
| 이메일 | 메일 호스팅 위치, MX·SPF·DKIM·DMARC, 메일함, 전달 설정, SMTP |
| 예약 작업 | cron, 큐, 워커, 데이터 가져오기·내보내기, 백업, 예약된 작업 |
| 외부 서비스 | 결제 웹훅, API, 허용 IP 목록, CDN·WAF, 분석 도구, Search Console |
| 보안·비밀정보 | 환경 변수, API 키, SSH 키, TLS, 방화벽 규칙 |

필요하지 않은 변경까지 한꺼번에 묶지 마세요. 호스팅을 옮기는 동시에 도메인, URL 구조, 애플리케이션 버전, 주요 소프트웨어까지 모두 바꾸면 장애 원인을 추적하기 어려워집니다.

## DNS 전환 전 준비 상태 점검 {#migration-cutover-preflight}

DNS를 변경하기 전에 아래 점검 도구를 사용하세요. 성공적인 이전을 보장하는 도구는 아닙니다. 먼저 해결해야 할 누락 사항을 확인하는 데 사용합니다.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="migration-preflight">
  <div class="mb-6">
    <label for="mig-backup" class="form-label">독립된 백업이 있고 복원 또는 가져오기를 테스트했습니다</label>
    <select id="mig-backup" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-sizing" class="form-label">새 VPS의 CPU·RAM·디스크 용량에 여유분을 반영했습니다</label>
    <select id="mig-sizing" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-runtime" class="form-label">런타임·데이터베이스·필수 확장 모듈의 호환성을 확인했습니다</label>
    <select id="mig-runtime" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-test" class="form-label">DNS 전환 전에 새 사이트를 비공개 환경에서 테스트했습니다</label>
    <select id="mig-test" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-dns" class="form-label">DNS 레코드를 기록하고 TTL 및 전환 계획을 세웠습니다</label>
    <select id="mig-dns" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-mail" class="form-label">메일 서비스의 위치와 MX·SPF·DKIM·DMARC 처리 방식을 정했습니다</label>
    <select id="mig-mail" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option><option value="na">해당 없음 / 메일이 별도 서비스에 있고 변경하지 않음</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-writes" class="form-label">주문·양식·회원·업로드 데이터의 최종 쓰기 및 동기화 계획이 있습니다</label>
    <select id="mig-writes" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료 / 사실상 읽기 전용 사이트</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-tls" class="form-label">실제 호스트 이름으로 새 서버의 HTTPS/TLS가 작동하는지 확인했습니다</label>
    <select id="mig-tls" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-jobs" class="form-label">cron·워커·웹훅·허용 IP 목록을 파악하고 제어할 수 있습니다</label>
    <select id="mig-jobs" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option><option value="na">해당 없음</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-rollback" class="form-label">롤백 실행 조건을 정했고 기존 호스팅을 계속 사용할 수 있습니다</label>
    <select id="mig-rollback" class="form-input"><option value="no">미준비</option><option value="yes">준비 완료</option></select>
  </div>
  <button class="btn btn-primary" type="submit">전환 준비 상태 확인</button>
</form>
<p id="migration-preflight-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">실제로 준비된 항목만 준비 완료로 표시하세요.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("migration-preflight");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var items = [
      ["mig-backup", "독립 백업"],
      ["mig-sizing", "새 VPS 사양"],
      ["mig-runtime", "런타임·데이터베이스 호환성"],
      ["mig-test", "새 서버의 비공개 테스트"],
      ["mig-dns", "DNS·TTL 계획"],
      ["mig-mail", "메일·메일용 DNS 계획"],
      ["mig-writes", "최종 데이터 쓰기·동기화 계획"],
      ["mig-tls", "HTTPS·TLS 준비"],
      ["mig-jobs", "cron·워커·웹훅·허용 IP 목록"],
      ["mig-rollback", "롤백 계획"]
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
      result = "계획된 전환을 진행할 준비가 되었습니다. 필수 항목이 모두 준비되었거나 명시적으로 해당 없음으로 표시되어 있습니다. DNS 변경 직전에 최종 데이터 동기화와 롤백 실행 조건을 다시 확인하세요.";
    } else {
      result = "전환 준비가 완료되지 않았습니다. 먼저 다음 항목을 해결하세요: " + missing.join(", ") + ".";
    }

    document.getElementById("migration-preflight-result").textContent = result;
  });
});
</script>

## 기존 웹사이트 현황 조사 {#inventory-the-current-website}

새 서버를 구성하기 전에 이전 작업 기록을 만드세요.

다음 사항을 기록합니다.

- 도메인과 실제 사용 중인 모든 하위 도메인
- 애플리케이션·CMS·프레임워크 버전
- PHP, Node.js, Python 등 실행 환경의 버전
- 데이터베이스 엔진·버전, 크기, 자격 증명 관리 방식
- 문서 루트와 그 외부에 위치한 디렉터리
- 업로드·미디어 파일과 쓰기 가능한 디렉터리
- 리디렉션과 URL 재작성 규칙
- cron, 큐, 워커 및 예약 작업
- Redis 등 사용 중인 캐시 서비스
- SSL/TLS 설정
- DNS 레코드
- 메일함, 전달 설정, 발신 SMTP 경로
- 결제 게이트웨이, 웹훅, API 콜백
- 외부 서비스의 허용 IP 목록
- CDN·WAF 및 원본 서버 접근 제한
- Search Console·분석 도구 인증
- 현재 디스크 사용량과 증가 추세

이 목록은 이전 완료 후 검수 기준으로도 사용합니다. 각 항목이 새 VPS에서 정상 작동하거나, 외부 서비스에 의도적으로 남겨져 있어야 합니다.

## 대상 VPS 사양 산정 및 준비 {#size-and-prepare-the-destination-vps}

서버를 이전한 다음에야 VPS의 용량이 충분한지 확인해서는 안 됩니다.

현재 부하, 데이터베이스 동작, 저장 공간 증가량, 관리 패널·메일 서비스의 자원 사용량과 이전 중 작업 공간을 고려하세요. 압축 파일, DB 덤프, 로그, 로컬 백업 임시 보관에도 디스크 공간이 필요할 수 있습니다.

자원 계산은 여기서 반복하지 않고 [웹사이트용 VPS 사양]({{< relref "vps-sizing-for-website.md" >}})에서 안내합니다.

서버 이전은 운영 책임을 정하는 일이기도 합니다. 기존 호스팅이 서버 관리의 대부분을 대신했다면 전환 후 누가 새 서버를 운영할지 먼저 정하세요. [관리형 VPS와 자체 관리형 VPS 비교]({{< relref "managed-vs-unmanaged-vps.md" >}})를 참고하세요. 이후 관리 패널을 사용할지, Linux 스택을 직접 관리할지 결정해야 합니다. [VPS 관리 패널 선택]({{< relref "vps-with-control-panel.md" >}})에서 차이를 확인할 수 있습니다.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">이전할 VPS 사양 확인하기</a>
</p>
<p><small>제휴 안내: 운영자는 VDSina와 업무상 관계가 있으며, 이 제휴 링크를 통한 주문에서 수수료를 받을 수 있습니다. 이전 절차와 서버 사양 판단 기준은 수수료에 따라 달라지지 않습니다.</small></p>

## 롤백 가능한 백업 만들기 {#create-a-rollback-capable-backup}

백업은 필요한 데이터가 들어 있고 실제로 복원할 수 있을 때 의미가 있습니다.

이전 전에 다음을 수행하세요.

1. 웹사이트 파일을 최신 상태로 복사합니다.
2. 필요한 모든 데이터베이스를 내보냅니다.
3. 기존 호스팅 계정 외부에 백업 사본을 보관합니다.
4. 설정 파일과 환경 변수를 안전하게 기록합니다.
5. DNS와 메일 레코드를 별도로 기록합니다.
6. 가능하면 폐기 가능한 테스트 환경에 백업을 복원합니다. 어렵다면 적어도 실제 DB 가져오기를 수행하고 대표적인 파일을 확인하세요. 압축 파일이 열린다는 사실만으로 검증이 끝나지 않습니다.
7. 복원한 사본에 예상한 데이터가 있는지, 롤백에 사용할 수 있을 정도로 애플리케이션을 실행할 수 있는지 확인합니다.
8. DNS 변경 전에 롤백 절차를 문서화합니다.

동적 사이트의 첫 백업은 최종 운영 데이터가 아닙니다. 처음 복사한 뒤에도 주문, 양식 제출, 댓글, 회원 정보, 업로드 파일이 변경될 수 있으므로 마지막 변경분 동기화를 별도로 계획해야 합니다.

## DNS를 변경하기 전에 새 서버 구축하기 {#build-the-destination-before-dns-changes}

공개 트래픽을 받기 전에 새 서버에서 실제 사이트가 작동할 수 있어야 합니다.

다음 항목을 기존 환경과 맞추거나 차이를 의도적으로 검증하세요.

- 웹 서버의 동작 방식
- PHP·Node·Python 버전
- 필요한 확장 모듈
- 데이터베이스 엔진과 버전
- 파일 소유자 및 권한
- 업로드·요청 본문의 크기 제한
- 예약 작업의 실행 환경
- 캐시 서비스
- URL 재작성·리디렉션 규칙
- 환경 변수와 비밀정보
- SMTP·발신 네트워크 요구사항
- 방화벽 규칙
- 애플리케이션별 파일 경로

꼭 필요한 경우가 아니라면 이전하는 날에 모든 런타임을 업그레이드하거나 시스템 구성을 전면 교체하지 마세요. 동시에 바꾸는 요소가 적을수록 장애 진단과 롤백이 쉬워집니다.

## 파일과 데이터베이스 복사 {#copy-files-and-database}

전송 방법은 기존 호스팅에서 제공하는 접근 권한에 따라 달라집니다.

일반적인 방법은 다음과 같습니다.

- cPanel·파일 관리자의 다운로드와 phpMyAdmin 내보내기
- 셸 접근 권한이 없을 때 SFTP·FTP 사용
- 양쪽 서버에서 지원한다면 SSH·rsync 사용
- CMS 특성에 맞춘 애플리케이션 전용 이전 도구
- 호스팅 업체의 내보내기·백업 기능

애플리케이션에 필요한 URL 재작성 설정 등 숨김 구성 파일도 보존하세요. DB 가져오기 후에는 사용자, 권한, 문자 집합·정렬 규칙의 전제조건, 애플리케이션 연결 설정을 검증해야 합니다.

데이터가 많다면 전송 완료 메시지에만 의존하지 말고 가능할 때 파일 크기, 행 수 또는 체크섬을 비교하세요.

## 전환 전 비공개 테스트 {#test-privately-before-cutover}

테스트하지 않은 서버로 DNS를 돌리지 마세요.

hosts 파일의 호스트 이름 매핑, 통제된 미리보기 호스트 이름 등 **새 서버에서 실제 애플리케이션 스택을 실행하는 방식**으로 확인하세요.

검사할 항목:

- 메인 페이지와 대표적인 내부 페이지
- 관리자 로그인
- 사용자 로그인
- 이미지·CSS·JavaScript·다운로드
- 검색 기능
- 양식 제출과 알림 전달
- 파일 업로드
- 리디렉션
- API 엔드포인트
- 주문·결제·결제 서비스 콜백
- cron·예약 작업
- 큐·워커
- 발신 메일
- 애플리케이션·웹 서버·데이터베이스 로그
- 모바일 화면과 메뉴 탐색

임시로 공개한 미리보기 호스트가 검색 결과에서 중복 사이트로 색인되지 않게 주의하세요. 테스트 환경이 공개 접근 가능한 경우 색인을 차단하고, 실제 운영 호스트로 전환하기 전에 임시 차단이 남아 있지 않도록 확인해야 합니다.

## 새로운 데이터 쓰기 통제와 최종 동기화 {#control-new-writes-and-the-final-sync}

단순 소개 사이트와 주문·거래가 발생하는 사이트의 이전에서 가장 중요한 차이점입니다.

DNS 전환 중 기존 DB와 새 DB가 **모두 쓰기를 허용하면 데이터가 서로 달라질 수 있습니다**. 기존 서버에 저장된 주문이 새 서버에 자동으로 복사되는 것은 아닙니다.

데이터가 변경되는 사이트에서는 다음 절차를 따릅니다.

1. 위험이 적은 전환 시간을 정합니다.
2. 가능하면 기존 사이트의 새로운 데이터 쓰기를 일시 중지하거나 통제합니다.
3. 같은 데이터를 두 번 쓰는 cron·큐 워커의 실행을 중지하거나 제어합니다.
4. 최종 DB 변경분을 동기화하고 바뀐 업로드·파일을 복사합니다.
5. 어느 시점의 데이터를 최종 기준으로 삼았는지 기록합니다.
6. 트래픽을 새 서버로 전환합니다.
7. 새로운 쓰기 작업이 이제 새 서버에만 저장되는지 확인합니다.

[WooCommerce용 VPS]({{< relref "vps-for-woocommerce.md" >}})를 이전한다면 결제, 주문, 결제 웹훅, 재고, 예약 작업과 거래 관련 메일을 검수에 포함하세요. 정적·캐시 중심 사이트라면 마지막 파일 비교만으로 충분할 수 있습니다.

애플리케이션과 동기화 방법이 실제 무중단 전환을 지원하지 않는데도 '무중단 이전'이라고 보장해서는 안 됩니다.

## 계획에 따라 DNS 전환하기 {#switch-dns-deliberately}

DNS는 **트래픽을 전환하는 수단**이지 이전 작업의 시작점이 아닙니다.

전환 전에 다음을 확인하세요.

- 현재 DNS 영역을 내보내거나 레코드 전체를 기록합니다.
- 변경해야 할 A·AAAA·CNAME·원본 서버 레코드를 정확히 구분합니다.
- 가능하면 전환 예정 시각보다 최소한 기존 TTL 한 주기 앞서 해당 TTL을 낮춥니다. 예를 들어 기존 TTL이 86,400초라면 전환 24시간보다 더 일찍 줄여야 합니다.
- TTL을 지금 낮춰도 이미 오래된 TTL로 캐시된 응답이 즉시 삭제되지는 않는다는 점을 기억합니다.
- 이전 대상이 아닌 MX·SPF·DKIM·DMARC·TXT 인증·SRV·CAA 등 모든 관련 레코드를 보존합니다.
- 루트 도메인과 www 양쪽의 동작을 확인합니다.

DNS 서비스 업체 자체를 바꾸지 않는다면 네임서버 전체 교체보다 필요한 A·AAAA 레코드만 변경하는 편이 일반적으로 위험이 적습니다. 네임서버를 바꿔야 한다면 필요한 DNS 영역 전체를 먼저 새 환경에 재현하세요.

전환 뒤에는 두 개 이상의 DNS 리졸버나 네트워크에서 공개 레코드를 확인하고, 트래픽이 기존 서버에서 새 서버로 이동하는 과정을 모니터링하세요.

## 메일 서비스가 중단되지 않도록 관리하기 {#keep-email-from-breaking}

기존 공유 호스팅 계정에 웹사이트와 메일이 함께 포함되어 있더라도 **웹사이트 이전과 이메일 이전은 서로 다른 작업**입니다.

DNS 전환 전에 다음 가운데 하나를 선택하세요.

- 현재 업체나 관리형 메일 서비스를 유지하고 기존 MX·TXT 레코드를 보존합니다.
- 다른 관리형 메일 서비스로 이전합니다.
- 메일을 VPS로 옮기고 메일함, 라우팅, 인증 및 발신 신뢰도 관리를 다시 구성합니다.

메일도 이전한다면 다음을 확인합니다.

- MX 우선순위
- SPF
- DKIM
- DMARC
- 해당하는 경우 역방향 DNS·PTR
- 메일함 데이터
- 별칭·메일 전달 설정
- SMTP 자격 증명
- 스팸 필터링
- 백업과 발신자 평판

웹사이트만 이전하려고 DNS 영역 전체를 교체하지 마세요. 불가피하다면 메일을 포함한 모든 의존 레코드가 새 영역에 재현되어야 합니다.

## HTTPS·CDN·외부 서비스 검증 {#verify-https-cdn-and-external-services}

새 서버를 어느 리전에 둘지 정하지 않았다면 전환 전에 [VPS 서버 위치 선택]({{< relref "how-to-choose-vps-location.md" >}})을 검토하세요. 나중에 리전을 바꾸면 IP·DNS 이전이 한 번 더 필요할 수 있습니다.

IP 주소로 정상 표시되는 새 서버도 실제 도메인에서는 실패할 수 있습니다.

확인할 사항:

- TLS 인증서가 필요한 모든 호스트 이름을 포함하는지
- HTTP에서 HTTPS로 올바르게 리디렉션되는지
- 루트 도메인과 www 사이의 canonical 동작이 바뀌지 않았는지
- HSTS 설정의 전제조건을 이해했는지
- CDN·WAF가 새 원본 서버를 가리키거나 접근을 허용하는지
- 프록시 사용 시 실제 방문자 IP가 올바르게 처리되는지
- 결제 웹훅이 새 원본 서버에 도달하는지
- 기존 서버 IP를 허용 목록에 넣었던 API 업체의 설정을 갱신했는지
- 새 서버에서 SMTP·API 자격 증명이 유효한지

임시 방화벽·WAF 예외는 필요한 범위로 제한하고, 이전 검수가 끝나면 제거하세요.

## URL을 유지하면서 SEO 신호 보존하기 {#preserve-seo-when-urls-stay-the-same}

순수한 호스팅 이전은 대개 공개 URL이 그대로 유지됩니다. 이때 SEO 점검의 핵심은 리디렉션 설계보다 **기존 상태와 새 상태의 일치 여부**입니다.

DNS 전환 전후에 다음을 비교하세요.

- HTTP 상태 코드
- canonical URL
- robots.txt
- meta robots와 실수로 추가된 noindex
- sitemap에 포함된 URL
- 내부 링크
- 중요한 구조화 데이터
- 페이지 콘텐츠와 실제 표시되는 리소스
- Search Console의 소유권 인증
- Googlebot과 일반 방문자에 대한 서버 응답

Google Search Central은 새 호스팅을 먼저 준비·테스트하고, 준비가 되었을 때만 DNS를 변경하고, 기존·새 호스팅을 모니터링하며, 트래픽 이전이 끝난 후 기존 인프라를 종료하도록 권고합니다. DNS TTL을 미리 낮추고 Search Console 인증이 유지되도록 하는 것도 권고합니다.

도메인과 URL을 유지한 채 서버만 바꾼다면 **Google Search Console의 주소 변경(Change of Address) 도구를 사용하지 마세요.** 이 도구는 도메인 이전에 사용하는 것이며 동일 URL의 호스팅 변경용이 아닙니다.

도메인이나 URL 경로까지 변경된다면 기존 URL과 새 URL을 하나씩 매핑하고 서버 측 영구 리디렉션을 적용하세요. 이는 동일 URL의 VPS 이전과 다른 사이트 이전 작업입니다.

## DNS 전환 직전 체크리스트 {#cutover-checklist}

DNS 레코드를 수정하기 직전에 확인하세요.

| 항목 | 통과 기준 |
|---|---|
| 백업 | 외부 사본이 있고 복원·가져오기 테스트와 대표 데이터 검증을 완료함 |
| 새 서버 | 실행 환경·DB·권한·비밀정보가 올바름 |
| 비공개 테스트 | 페이지, 양식, 로그인, 해당하는 경우 결제·API 테스트를 통과함 |
| 최종 데이터 | 마지막 DB·업로드 변경분을 동기화하고 최종 기준 시각을 기록함 |
| 예약 작업 | 기존 cron·워커를 제어했고 새 작업이 의도한 시점에 시작됨 |
| DNS | 변경할 레코드를 확정하고 메일·인증 레코드를 보존함 |
| HTTPS | 새 서버가 실제 호스트 이름으로 안전하게 응답함 |
| 외부 서비스 | 웹훅, 허용 IP, CDN·WAF, SMTP를 확인함 |
| SEO 일치 | canonical·robots·sitemap·상태 코드가 의도한 대로 일치함 |
| 롤백 | 실행 조건, 담당 조치, 기존 호스팅 유지 범위를 정함 |

'파일 전송이 끝났다'는 이유만으로 DNS를 바꾸지 마세요. 새 서버가 검수 기준을 충족해야 전환할 수 있습니다.

## 이전 후 검수 및 롤백 {#post-migration-acceptance-and-rollback}

DNS 변경 후에는 다음을 수행합니다.

- 기존·새 서버의 접근 로그와 오류 로그를 모두 확인합니다.
- 새로운 사용자 활동이 새 서버의 데이터베이스에 저장되는지 확인합니다.
- 양식, 결제, 로그인과 업로드를 다시 테스트합니다.
- cron, 큐, 예약 작업이 제대로 실행되는지 확인합니다.
- 해당하면 발신 메일과 수신 메일 라우팅을 확인합니다.
- CPU·RAM·디스크 및 DB 사용량을 모니터링합니다.
- HTTPS와 CDN·WAF 동작을 재확인합니다.
- 핵심 URL의 HTTP 200 및 리디렉션 동작이 이전과 같은지 확인합니다.
- Search Console의 크롤링·색인 신호를 확인합니다.
- 합의한 안정화·롤백 기간이 끝날 때까지 기존 환경을 유지합니다.

### 롤백에는 데이터 기준 시점이 있습니다 {#rollback-has-a-data-boundary}

초기에는 기존 서버가 여전히 **유효한 최신 데이터 원본일 때만** DNS를 되돌리는 것으로 복구할 수 있습니다.

그러나 새 서버에 주문, 회원 가입, 댓글 또는 업로드가 기록된 뒤 DNS만 기존 서버로 되돌리면 새 데이터가 누락될 수 있습니다. 이때는 데이터를 맞추거나 미리 계획한 별도의 동기화가 필요합니다.

이전 전에 롤백을 시작할 조건을 정하세요. 예를 들면 다음과 같습니다.

- 광범위한 5xx 오류
- 결제·주문 처리 실패
- DB 손상 또는 데이터 쓰기 누락
- 심각한 런타임 호환성 문제
- 인증·로그인 장애
- 정해진 시간 안에 해결할 수 없는 주요 메일·웹훅 장애

## 워드프레스·우커머스·맞춤형 애플리케이션 이전 참고사항 {#wordpress-woocommerce-and-custom-application-notes}

### 워드프레스 {#wordpress}

PHP 버전·확장 모듈, DB 호환성, 업로드, 재작성 규칙, wp-cron, 캐시, SMTP·문의 양식, 관리자 로그인을 확인하세요. 직렬화된 데이터를 손상시킬 수 있는 무분별한 문자열 검색·치환은 피하고, 필요한 경우 워드프레스 구조를 이해하는 도구를 사용하세요.

자원 사용 특성은 [워드프레스용 VPS]({{< relref "vps-for-wordpress.md" >}})에서 확인하세요.

### 우커머스와 기타 거래 처리 사이트 {#woocommerce-and-other-transactional-sites}

주문, 재고, 결제 콜백, 세션, 예약 작업, 거래 관련 이메일은 계속 변경되는 운영 데이터로 취급하세요. 최초 DB 복사본에만 의존하지 말고 마지막 데이터 쓰기 전환과 동기화를 계획해야 합니다.

자세한 내용은 [우커머스용 VPS]({{< relref "vps-for-woocommerce.md" >}})를 참고하세요.

### 맞춤형 애플리케이션 {#custom-applications}

환경 변수, 비밀정보, 백그라운드 워커, 큐, 빌드·런타임 버전, 객체 스토리지, 파일 경로, 웹훅, API 허용 IP 목록, 배포·시작 동작을 문서화하세요. IP 주소 응답만 확인하지 말고 실제 호스트 이름으로 테스트하세요.

## 기술 참고 자료 {#technical-references}

- Google Search Central: 웹 호스팅 변경과 SEO
- Google Search Central: URL 변경을 수반하는 사이트 이전

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">이전에 사용할 VPS 사양 확인하기</a>
</p>
<p><small>제휴 안내: 운영자는 VDSina와 업무상 관계가 있습니다. 제휴 링크에는 sponsored 속성이 지정되어 있습니다. VPS 요금·트래픽 제공량 및 기타 조건은 바뀔 수 있으므로 주문 전에 최신 조건을 확인하세요.</small></p>

## 자주 묻는 질문 {#faq}

### 도메인을 변경하지 않고 웹사이트를 VPS로 이전할 수 있나요? {#can-i-migrate-a-website-to-a-vps-without-changing-the-domain}

가능합니다. 호스팅을 바꾸면서도 도메인과 공개 URL은 그대로 유지할 수 있습니다. 먼저 새 서버를 구축·테스트한 후 DNS 레코드를 변경해 트래픽을 새 서버로 전달하세요.

### 웹사이트를 VPS로 옮길 때 301 리디렉션이 필요한가요? {#do-i-need-301-redirects-when-moving-a-website-to-a-vps}

공개 URL이 그대로라면 필요하지 않습니다. 도메인, 프로토콜·경로 또는 콘텐츠 구조가 바뀌어 실제 URL이 달라지는 경우에 리디렉션이 필요합니다.

### VPS 이전 중 서비스 중단 시간을 줄이려면 어떻게 해야 하나요? {#how-do-i-reduce-downtime-during-a-vps-migration}

기존 서버와 별개로 새 환경을 준비하고, 미리 관련 DNS TTL을 낮추고, 비공개 테스트를 완료하세요. 최종 데이터 쓰기를 통제해 동기화한 뒤 검수에 통과했을 때만 DNS를 바꾸고 전파 기간에는 기존 서버를 유지하세요.

### 이메일도 VPS로 함께 옮겨야 하나요? {#should-i-move-email-to-the-vps-too}

그럴 필요는 없습니다. 관리형 메일 서비스를 유지하면 이전 과정과 메일 전달 안정성에 따른 위험을 줄일 수 있습니다. 메일도 이전한다면 MX·SPF·DKIM·DMARC, 메일함 데이터, 해당하는 경우 역방향 DNS와 백업을 별도로 계획하세요.

### DNS를 바꾸기 전에 무엇을 테스트해야 하나요? {#what-should-i-test-before-changing-dns}

대표 페이지, 로그인, 양식, 업로드, 검색, 해당하는 경우 결제·결제 콜백, 예약 작업, API·웹훅, 발신 메일, HTTPS, 리디렉션과 애플리케이션·서버 로그를 검사하세요.

### 이전 후 기존 호스팅은 얼마나 유지해야 하나요? {#how-long-should-i-keep-the-old-hosting-after-migration}

DNS 트래픽이 이동하고 새 서버가 안정적으로 작동하며 새로운 데이터 쓰기가 확인되고 합의한 롤백 기간이 지날 때까지 유지하세요. 모든 사이트에 동일한 시간·일수를 적용하지 말고 로그를 기준으로 판단하세요.

### 주문을 잃지 않고 WooCommerce를 이전할 수 있나요? {#can-i-migrate-woocommerce-without-losing-orders}

가능하지만 오래된 DB 사본 하나만으로는 부족합니다. 전환 중 데이터 쓰기를 통제하고 애플리케이션 특성에 맞는 최종 동기화를 실행해야 주문과 재고 변경이 서로 다른 두 DB에 나뉘어 저장되지 않습니다.

### 서버 호스팅을 옮기면 SEO에 악영향이 있나요? {#does-moving-hosting-hurt-seo}

URL을 바꾸지 않는 호스팅 이전이라면 새 서버가 동일한 콘텐츠, 상태 코드, canonical과 크롤링 접근성을 제공하도록 유지해야 검색 신호를 보존할 수 있습니다. 이전 후 Search Console과 서버 로그를 모니터링하세요. 인프라 변경 중에는 크롤링 빈도가 일시적으로 달라질 수 있습니다.
