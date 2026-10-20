---
title: "VPS 모니터링"
slug: "vps-모니터링"
draft: true
description: "외부 가용성 점검, CPU·RAM·디스크·네트워크 지표, 서비스 상태, 로그와 대응 가능한 알림을 통해 VPS를 모니터링하는 방법. 도구, 임계값과 실무 체크리스트를 다룹니다."
image: "images/home/vps-for-website-hero.webp"
---

VPS 모니터링은 단순히 “서버가 켜져 있는가?”에 답하는 데 그쳐서는 안 됩니다. 운영 환경의 기본 모니터링에는 **외부 가용성 점검, 과거 서버 지표, 서비스와 애플리케이션 상태, 로그, 대응 가능한 알림, 명확히 지정된 담당자**가 필요합니다.

Nginx에 장애가 생기거나 데이터베이스가 멈추고 디스크가 가득 찼거나 TLS 인증서가 만료 직전이어도 VPS는 ping에 응답할 수 있습니다. 따라서 모니터링은 서버 자체뿐 아니라 사용자가 접속하는 웹사이트도 확인해야 합니다.

서버 선택의 전반적인 기준은 [웹사이트용 VPS]({{< relref "_index.md" >}})를 참고하세요.

[핵심 요약](#quick-answer) · [진단 도구](#vps-monitoring-baseline-checker) · [서버 지표](#monitor-cpu-memory-disk-and-network) · [애플리케이션 상태](#monitor-services-and-application-health) · [알림](#build-actionable-alerts) · [용량 계획](#use-trends-for-capacity-planning) · [FAQ](#faq)

## 핵심 요약 {#quick-answer}

실용적인 VPS 모니터링 구성은 다섯 계층으로 이루어집니다.

| 계층 | 확인할 수 있는 사항 | 감지할 수 있는 대표적인 장애 |
|---|---|---|
| **외부 가용성** | 사용자가 VPS 외부에서 웹사이트에 접속할 수 있는지 | VPS·네트워크·웹사이트 접속 불가 |
| **서버 지표** | CPU, RAM, 스왑, 디스크, inode, I/O, 네트워크의 추세 | 메모리 누수, 디스크 포화, 지속적인 CPU 부하 |
| **서비스·애플리케이션 상태** | 웹 서버, 실행 환경, DB와 핵심 엔드포인트가 실제로 작동하는지 | 서버는 온라인이지만 Nginx·PHP·DB·앱에 장애가 발생하는 상황 |
| **로그·이벤트** | 무엇이 변경되거나 실패했는지 | 5xx 급증, OOM, 워커 실패, DB 오류 |
| **알림 및 담당자** | 적절한 담당자에게 통보되어 조치할 수 있는지 | 아무도 모르는 장애 또는 방치된 대시보드 |

가용성 확인 도구를 감시 대상과 동일한 VPS에서만 실행하지 마세요. VPS나 네트워크 경로가 완전히 장애를 일으키면 감시 도구도 함께 중단될 수 있습니다.

## VPS 모니터링 기본 구성 진단 {#vps-monitoring-baseline-checker}

이 진단 도구로 모니터링 사각지대를 찾을 수 있습니다. 가동 시간을 보장하는 도구는 아닙니다.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">주요 워크로드</label>
    <select id="mon-workload" class="form-input">
      <option value="static">정적 / 단순 웹사이트</option>
      <option value="cms">WordPress / CMS</option>
      <option value="transactional">WooCommerce / 거래 처리 웹사이트</option>
      <option value="multi">여러 웹사이트 / 혼합 운영 환경</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">VPS 외부에서 HTTP(S) 가용성을 확인하고 있나요?</label>
    <select id="mon-external" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">CPU/RAM/디스크/네트워크의 과거 지표를 보존하나요?</label>
    <select id="mon-metrics" class="form-input"><option value="no">No / only ad-hoc top/htop</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">디스크 용량, inode와 스토리지 부하를 감시하나요?</label>
    <select id="mon-disk" class="form-input"><option value="no">No / only free GB</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">핵심 서비스와 애플리케이션 상태 점검이 설정되어 있나요?</label>
    <select id="mon-app" class="form-input"><option value="no">No / only ping</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">해당하는 경우 DB / 큐 / cron / 최근 백업 상태를 감시하나요?</label>
    <select id="mon-jobs" class="form-input"><option value="no">No / unknown</option><option value="yes">Yes</option><option value="na">Not applicable</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">심각도와 지속 시간 조건을 적용한 자동 알림이 있나요?</label>
    <select id="mon-alerts" class="form-input"><option value="no">No / dashboard only</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">이 VPS가 중단되어도 알림 경로가 유지되나요?</label>
    <select id="mon-notify" class="form-input"><option value="no">No / same VPS only</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">지정된 담당자와 최초 대응 절차서가 있나요?</label>
    <select id="mon-owner" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <button class="btn btn-primary" type="submit">모니터링 기본 구성 점검</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">실제로 데이터를 수집하고 알림을 전달하는 항목만 선택하세요.</p>
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
      result = "사각지대 발견: 기본적인 장애 유형 중 일부를 아직 감지할 수 없습니다. 독립적인 가용성 점검, 과거 서버 지표, 디스크와 inode 모니터링, 실제 서비스 및 애플리케이션 상태 점검을 추가하세요.";
    } else if (!alerts || !notify || !owner) {
      result = "알림 / 책임 체계 미흡: 지표를 수집하더라도 장애가 감지되지 않거나 담당자가 없을 수 있습니다. 대응 가능한 알림, 독립적인 알림 경로와 담당자가 명시된 대응 절차서를 마련하세요.";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "기본 모니터링: 인프라 감시는 마련되어 있지만 이 워크로드의 애플리케이션 작업, 데이터베이스 또는 최근 백업 상태는 여전히 사각지대입니다.";
    } else {
      result = "운영 환경의 기본 모니터링 확보: 외부 가용성, 과거 지표, 서비스 상태, 알림과 대응 담당자가 마련되어 있습니다. 실제 정상 상태를 기준으로 임계값을 계속 조정하세요. 가동 시간을 보장하지는 않습니다.";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## VPS 외부에서 웹사이트 모니터링 {#monitor-the-website-from-outside-the-vps}

내부 명령으로 Nginx가 실행 중인지 확인할 수는 있습니다. 하지만 인터넷의 실제 사용자가 웹사이트에 접속할 수 있는지는 증명하지 못합니다.

중요한 호스트 이름에는 외부 감시 도구를 사용하세요.

유용한 점검 항목은 다음과 같습니다.

- HTTP/HTTPS 가용성;
- 예상한 상태 코드;
- 응답 시간;
- 키워드·콘텐츠 점검;
- DNS 이름 해석;
- TLS 인증서 상태·만료일;
- 필요한 경우 TCP 포트 점검.

오탐의 영향이 크다면 담당자를 호출하기 전에 장애가 반복되는지 또는 둘 이상의 지역에서 동일한 문제가 확인되는지 검증하세요.

Uptime Kuma 같은 자체 호스팅 도구는 HTTP(S), 키워드, TCP, ping 및 DNS를 점검할 수 있습니다. 다만 감시 시스템은 운영 VPS와 독립된 장애 영역에 배치해야 합니다.

같은 VPS, 제공업체 네트워크 또는 DNS 장애에 영향을 받는 감시 서버는 대시보드 용도로 유용할 수 있지만 독립적인 가용성 점검으로 볼 수는 없습니다.

## 실시간 진단은 과거 지표 모니터링과 다릅니다 {#real-time-diagnostics-are-not-historical-monitoring}

다음과 같은 명령은:

```bash
top
htop
free -h
df -h
ss -s
```

이미 발생한 문제를 조사할 때 유용합니다.

그러나 다음 정보는 알려주지 못합니다.

- 03:12에 무슨 일이 있었는지;
- RAM 사용량이 6시간 동안 지속적으로 증가했는지;
- 백업 중 디스크 지연 시간이 급증했는지;
- 웹사이트가 10분 동안 중단되었는지;
- 문제가 주마다 악화되고 있는지.

가용성과 용량에 영향을 주는 지표는 시계열 이력을 보존하세요.

VPS 한 대라면 가벼운 모니터링 에이전트만으로 충분할 수 있습니다. 여러 서버, 장기 보존 또는 맞춤형 대시보드가 필요하면 Prometheus + Node Exporter + Grafana 구성이 흔히 사용됩니다.

Prometheus Node Exporter는 CPU, 파일시스템과 네트워크 데이터를 포함한 호스트·커널 지표를 Prometheus가 수집할 수 있도록 제공합니다.

## CPU, 메모리, 디스크와 네트워크 모니터링 {#monitor-cpu-memory-disk-and-network}

### CPU {#cpu}

짧은 사용량 급증마다 알림을 보내지 마세요.

다음 지표를 확인하세요.

- 장시간 지속되는 CPU 사용률;
- vCPU 개수 대비 평균 부하;
- 프로세스별 CPU 사용량;
- 가상화 환경에서 제공하는 경우 CPU steal time;
- 같은 시점의 애플리케이션·요청 지연 시간.

캐시 준비나 cron 작업 중 잠시 CPU가 100%에 도달하는 것은 문제가 아닐 수 있습니다. CPU 포화가 지속되면서 지연 시간과 큐가 함께 증가한다면 실제 병목의 근거가 됩니다.

### 메모리, 스왑과 OOM {#memory-swap-and-oom}

Linux는 남는 RAM을 파일시스템 캐시로 사용하므로 “RAM 사용률 90%”가 반드시 장애를 뜻하지는 않습니다.

다음 지표를 확인하세요.

- 사용 가능한 메모리;
- 스왑 활동;
- 스왑 사용량 증가;
- OOM-killer 발생 기록;
- 프로세스 메모리 사용량 증가;
- PHP·애플리케이션 워커의 메모리;
- 데이터베이스 메모리.

메모리 누수는 낮에는 정상처럼 보이다가 밤사이 프로세스를 종료시킬 수 있습니다. 이런 문제는 과거 추세 데이터로 확인합니다.

### 디스크 용량 {#disk-capacity}

데이터베이스, 로그 또는 패키지 업데이트가 실패할 정도로 공간이 부족해지기 전에 파일시스템 사용률을 감시하세요.

경고·위험 임계값의 예시로 **사용률 80% / 90%**를 둘 수 있지만 보편적인 SLA는 아닙니다. 빠르게 증가하는 데이터베이스에는 훨씬 이른 조치가 필요할 수 있습니다.

다음 작업에 필요한 여유 공간도 감시하세요.

- 백업;
- 데이터베이스 유지 관리;
- 패키지 업데이트;
- 업로드;
- 로그;
- 스테이징 및 가져오기 작업.

### Inode {#inodes}

디스크에 수 GB가 남아 있어도 파일시스템의 inode가 소진될 수 있습니다.

다음과 같은 경우에 발생할 수 있습니다.

- 캐시 디렉터리;
- 세션;
- 메일 큐;
- 매우 많은 작은 파일;
- 통제되지 않고 쌓이는 임시 파일.

디스크의 잔여 GB와 inode 사용량을 별도로 추적하세요.

### 디스크 I/O와 지연 시간 {#disk-io-and-latency}

저장 공간이 가득 차기 전에 디스크가 병목이 될 수 있습니다.

다음 지표를 확인하세요.

- I/O 대기 시간;
- 읽기·쓰기 지연 시간;
- 확인할 수 있다면 큐 깊이;
- 데이터베이스 응답 시간;
- 백업·가져오기 수행 시간대.

디스크 용량을 늘리는 것만으로 느린 스토리지 I/O가 해결되지는 않습니다.

### 네트워크 {#network}

총 대역폭 외에도 다음을 추적하세요.

- 인바운드·아웃바운드 처리량;
- 갑작스러운 트래픽 변화;
- 연결 오류;
- 측정 가능한 경우 패킷 손실과 지연 시간;
- 비정상적인 아웃바운드 트래픽;
- 네트워크 인터페이스 오류.

네트워크 지표를 통해 애플리케이션 자체의 지연과 제공업체·전송 경로의 문제를 구분할 수 있습니다.

## 서비스와 애플리케이션 상태 모니터링 {#monitor-services-and-application-health}

VPS에 접속할 수 있어도 웹사이트는 정상 작동하지 않을 수 있습니다.

다음과 같은 주요 서비스를 감시하세요.

- Nginx/Apache;
- PHP-FPM;
- Node/Python 애플리케이션 서비스;
- MySQL/MariaDB/PostgreSQL;
- 사용하는 경우 Redis;
- 큐 워커;
- 예약 작업 서비스;
- 업무상 중요한 경우 컨트롤 패널.

systemd 기반 Linux에서는 진단 시 `systemctl --failed`가 유용합니다. 하지만 상시 모니터링은 필수 서비스가 실패하거나 반복 재시작할 때 알림을 보내야 합니다.

“프로세스가 존재한다”는 확인만으로 끝내지 마세요. 프로세스가 살아 있어도 정상적인 요청을 처리하지 못할 수 있습니다.

## HTTP 200만으로 정상 상태를 보장할 수 없습니다 {#http-200-is-not-always-healthy}

애플리케이션이 HTTP 200을 반환하면서도 다음 상태일 수 있습니다.

- 점검 안내 페이지만 표시;
- 템플릿 내부에 데이터베이스 오류 표시;
- 콘텐츠가 비어 있거나 잘못됨;
- 로그인 절차 장애;
- 오래된 캐시 제공.

중요한 사이트에는 필요한 기능을 정확히 검증하는 점검을 사용하세요.

- 예상한 키워드·문구;
- 상태 확인 엔드포인트;
- API 응답;
- 핵심 공개 URL;
- 업무상 가치가 추가 복잡성을 정당화하는 경우에만 합성 로그인·거래 테스트.

안전하게 변경하도록 설계된 테스트가 아니라면 합성 점검으로 운영 데이터를 수정하지 마세요.

## TLS와 DNS 모니터링 {#monitor-tls-and-dns}

VPS가 정상이어도 인증서 또는 DNS 장애 때문에 웹사이트에 접속하지 못할 수 있습니다.

다음을 추적하세요.

- 인증서 만료일;
- 인증서와 호스트 이름 불일치;
- 갱신 실패;
- DNS 이름 해석;
- 도구가 지원하는 경우 의도하지 않은 DNS 레코드 변경.

예를 들어 인증서 만료 **14일** 전에 미리 경고하고, **7일** 전에는 경고 수준을 높일 수 있습니다. 실제 알림 기간은 담당자가 갱신 문제를 해결하는 데 필요한 시간에 맞춰야 합니다.

## 애플리케이션 의존 요소인 데이터베이스 모니터링 {#monitor-the-database-as-an-application-dependency}

데이터베이스를 사용하는 웹사이트에서는 DB가 병목인지, 아니면 장애가 발생한 의존 서비스인지 구분할 수 있도록 감시해야 합니다.

엔진과 워크로드에 따라 다음 지표가 유용합니다.

- 서비스 가용성;
- 연결 수;
- 연결 오류;
- 쿼리 지연 시간;
- 잠금·경합 징후;
- 느린 쿼리 발생 현황;
- 메모리 압박;
- 저장 공간 증가;
- 사용하는 경우 복제·백업 상태.

DB 지표마다 알림을 보내지 마세요. 사용자에게 영향을 주거나 알려진 장애 유형과 관련된 조건에 대해 알리세요.

WordPress 워크로드의 특성은 [WordPress용 VPS]({{< relref "vps-for-wordpress.md" >}})를, 거래 처리형 쇼핑몰은 [WooCommerce용 VPS]({{< relref "vps-for-woocommerce.md" >}})를 참고하세요.

## cron, 큐와 백그라운드 작업 모니터링 {#monitor-cron-queues-and-background-jobs}

홈페이지가 정상이라고 해서 백그라운드 작업까지 정상인 것은 아닙니다.

애플리케이션에 중요한 다음 작업을 추적하세요.

- cron;
- 큐 워커;
- 예약된 데이터 가져오기;
- 웹훅;
- 이메일 작업;
- WordPress WP-Cron·시스템 cron;
- WooCommerce Action Scheduler;
- 구독·갱신;
- 재고 동기화.

유용한 지표:

- 마지막 성공 실행 시각;
- 큐 깊이·적체량;
- 실패한 작업;
- 가장 오래 대기 중인 작업;
- 반복되는 재시도;
- 워커 중지·재시작.

WooCommerce에서는 상품 목록 페이지가 열리더라도 Action Scheduler의 실패·지연 작업이 계속 쌓이면 운영상 문제가 될 수 있습니다.

## 최신 백업 상태 모니터링 {#monitor-backup-freshness}

백업 작업은 복구 전략의 일부이지만 **가장 최근 백업의 상태도 중요한 모니터링 지표**입니다.

다음 상황에 알림을 설정하세요.

- 예약된 백업 실패;
- 마지막 성공 백업이 정의된 RPO보다 오래됨;
- DB 덤프 실패;
- 외부 저장소 업로드 실패;
- 백업 저장소 자격 증명 만료;
- 백업 크기가 의심스럽게 변함;
- 오래된 백업 정리·보존 작업 실패.

“cron이 실행됐다”는 사실만으로 복원 가능한 백업이 있다고 판단하지 마세요.

RPO/RTO, 보존 기간, 독립적인 사본과 복원 훈련은 [VPS 백업 전략]({{< relref "vps-backup-strategy.md" >}})을 참고하세요.

## 로그와 지표 연관 분석 {#correlate-logs-with-metrics}

지표는 **무엇이 변했는지** 알려주고, 로그는 흔히 **왜 변했는지** 설명합니다.

같은 시간대의 다음 로그를 함께 비교하세요.

- Nginx/Apache 액세스·오류 로그;
- PHP-FPM·실행 환경 로그;
- 애플리케이션 로그;
- 데이터베이스 로그;
- 시스템 저널;
- 인증 로그;
- 백업·작업 로그.

예시:

- 14:03에 CPU 급증;
- 14:03에 5xx 응답 증가;
- 애플리케이션 로그에 DB 시간 초과 기록;
- DB 로그에 잠금 경합 기록.

이런 정보는 단순한 “CPU 사용률 높음” 알림보다 실제 조치에 도움이 됩니다.

사고를 조사할 수 있을 만큼 로그를 보존하되, 로그 때문에 운영 파일시스템이 가득 차지 않도록 하세요.

## 대응 가능한 알림 구성 {#build-actionable-alerts}

알림에는 어떤 장애가 발생했고 무엇부터 확인해야 하는지가 나타나야 합니다.

다음 구성을 우선하세요.

- **경고(warning)** — 사용자에게 영향을 주기 전에 조사;
- **위험(critical)** — 사용자 영향 또는 임박한 장애;
- 지속 시간·디바운스 — 1초짜리 급증마다 호출하지 않음;
- 그룹화·중복 제거 — 한 번의 장애로 40개 알림이 오지 않도록 설정;
- 영향을 받은 서버·서비스의 명확한 표시;
- 대시보드·로그·대응 절차서 링크;
- 알려진 첫 조치와 상위 담당자에게 넘기는 기준.

Prometheus Alertmanager는 알림을 그룹화하고 중복을 제거하며 적절한 수신자에게 전달하도록 설계된 시스템의 예입니다.

### 모든 환경에 같은 임계값을 적용하지 마세요 {#avoid-universal-thresholds}

임계값은 워크로드에 맞아야 합니다.

합리적인 초기 판단 기준의 예시는 다음과 같습니다.

- CPU: 한 번의 급증보다 지연 시간·큐 적체를 동반한 지속적인 높은 사용률;
- RAM: 단순한 “사용 RAM > 80%”보다 낮은 가용 메모리와 스왑·OOM;
- 디스크: 운영에 필요한 여유 공간이 남아 있을 때 조기 경고;
- TLS: 만료 며칠 전부터 경고;
- HTTP: 오탐이 중요하다면 반복된 실패 또는 여러 지역에서의 확인;
- 백업: 마지막 성공 백업이 RPO보다 오래됨;
- 5xx·지연 시간: 해당 애플리케이션의 평상시 기준에서 지속적으로 벗어남.

운영 환경의 정상적인 동작을 관찰한 뒤 임계값을 조정하세요.

## 독립적인 알림 경로 유지 {#keep-the-notification-path-independent}

알림을 전달하는 시스템이 동일한 장애로 중단되면 알림은 무용지물입니다.

가능하다면 중요한 알림을 VPS 외부 경로로 보내세요.

- 외부 이메일 제공업체;
- 외부 채팅·알림 서비스;
- 호스팅형 사고 대응 도구;
- 다른 장애 영역의 모니터링 인스턴스.

장애가 발생한 VPS 자체에 설치된 SMTP 서버나 대시보드에만 의존하지 마세요.

## 모든 알림에는 담당자와 대응 절차서가 필요합니다 {#every-alert-needs-an-owner-and-runbook}

알림을 만들기 전에 다음을 정하세요.

- 누가 알림을 받는가?
- 누가 조치할 권한이 있는가?
- 첫 진단 단계는 무엇인가?
- 어떤 대시보드·로그를 열어야 하는가?
- 언제 문제를 상위 담당자에게 넘기는가?
- 언제 알림을 일시 중지해도 안전한가?
- 업무 시간 외에는 어떻게 대응하는가?

아무도 대응 책임을 맡지 않는다면 모니터링 시스템은 장애를 알림 메시지로 바꾼 것에 불과합니다.

운영 책임을 정하는 전반적인 기준은 [관리형 VPS와 비관리형 VPS]({{< relref "managed-vs-unmanaged-vps.md" >}})를 참고하세요.

## 복잡도에 맞는 모니터링 도구 선택 {#choose-the-monitoring-stack-by-complexity}

관측 도구가 인기 있다는 이유만으로 대규모 플랫폼을 도입하지 마세요.

### 초기 계층으로 활용하는 제공업체 대시보드 {#provider-dashboard-as-a-starting-layer}

VPS 제공업체가 CPU, RAM, 디스크 또는 네트워크의 과거 지표를 제공한다면 서버 수준의 기본 자료로 활용하세요.

제공업체의 인프라 그래프와 완전한 웹사이트 모니터링을 혼동하면 안 됩니다. 이런 그래프만으로는 제공업체 외부에서의 공개 HTTP(S) 접근, 애플리케이션 콘텐츠, DB 상태, 백그라운드 작업, TLS 갱신 또는 알림 담당자를 검증하지 못할 수 있습니다.

제공업체 모니터링을 여러 근거 중 하나로 사용하고, 워크로드에 필요한 외부 점검과 애플리케이션 수준의 검사를 추가하세요.

### VPS 한 대를 위한 경량 구성 {#lightweight-single-vps-path}

실용적인 소규모 구성은 다음을 결합할 수 있습니다.

- 외부 가용성 감시 도구;
- Netdata 또는 다른 서버 지표 에이전트·대시보드;
- 시스템·애플리케이션 로그;
- 알림.

한 명의 운영자가 VPS 한 대 또는 소수를 관리할 때 적합합니다.

### Prometheus / Grafana 구성 {#prometheus-grafana-path}

다음이 필요한 경우 유용합니다.

- 여러 서버의 지표;
- 장기간의 이력 보존;
- 맞춤형 쿼리;
- 서비스·exporter 지표;
- 공유 대시보드;
- 체계적인 알림 규칙.

Node Exporter는 Linux 서버 지표를 제공하고, Prometheus는 이를 저장·조회하며, Grafana는 시각화합니다. Alertmanager는 알림을 전달·그룹화하고 중복을 제거할 수 있습니다.

### 호스팅형 모니터링 구성 {#hosted-monitoring-path}

다음과 같은 경우 유용합니다.

- 감시 시스템이 자체 VPS·제공업체와 독립적이어야 할 때;
- 모니터링 인프라의 운영 부담을 줄이고 싶을 때;
- 관리형 알림·당직 시스템 연동이 중요할 때.

모니터링 시스템 자체도 운영 인프라입니다. 위험을 줄이는 효과에 비례하는 수준의 복잡도를 유지하세요.

## 모니터링 시스템 보안 강화 {#secure-the-monitoring-stack}

모니터링 에이전트와 대시보드는 민감한 운영 정보를 노출할 수 있습니다.

다음 항목을 보호하세요.

- 대시보드;
- exporter;
- 지표 엔드포인트;
- API 토큰;
- 알림용 웹훅;
- 로그 저장 시스템.

명시적인 보안 접근 통제 체계 없이 Prometheus, Node Exporter, Grafana 또는 관리자 대시보드를 인터넷에 공개하지 마세요.

상황에 맞게 방화벽, 사설 네트워크, 리버스 프록시 인증을 사용하세요.

모니터링이 보안 강화를 대체하지는 않습니다. 서버의 기본 보안 설정은 [VPS 보안 점검표]({{< relref "vps-security-checklist.md" >}})를 참고하세요.

## 모니터링 자체의 자원 사용량도 중요합니다 {#monitoring-overhead-matters}

모니터링은 다음 자원을 소비합니다.

- RAM;
- CPU;
- 지표·로그 보존용 디스크;
- 네트워크;
- 백업 용량.

작은 에이전트의 자원 비용은 보통 낮지만, 장기간 보관하는 지표와 로그는 상당한 저장 공간을 요구할 수 있습니다.

모니터링 시스템 자체도 점검하세요.

- 에이전트·서비스 상태;
- 지표 수집 실패;
- 저장 공간 증가;
- 보존 기간;
- 알림 전달 여부.

디스크를 보호해야 할 관측 시스템이 오히려 디스크를 가득 채우지 않도록 하세요.

## 용량 계획에 과거 추세 활용 {#use-trends-for-capacity-planning}

과거 모니터링 데이터는 다음 서버 사양을 결정할 때 가장 유용한 근거입니다.

추세를 통해 다음 질문에 답하세요.

- CPU 포화가 지속되는가, 아니면 가끔 발생하는가?
- 몇 주 동안 사용 가능한 RAM이 줄어드는가?
- 정상적인 부하에서도 스왑·OOM이 발생하는가?
- 디스크 사용량은 얼마나 빨리 증가하는가?
- 트래픽이 집중될 때 DB 지연 시간이 늘어나는가?
- PHP·애플리케이션 큐가 쌓이는가?
- 백업·가져오기 작업이 예측 가능한 자원 경합을 일으키는가?

대시보드가 잠깐 빨간색으로 바뀌었다는 이유만으로 VPS를 업그레이드하지 마세요.

**최적화된 정상 워크로드**가 자원을 반복적으로 소진하거나 아키텍처상 독립적인 확장이 필요할 때 확장하세요.

측정 데이터를 자원 결정에 반영하는 방법은 [웹사이트용 VPS 사양 선택]({{< relref "vps-sizing-for-website.md" >}})을 참고하세요.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">현재 VPS 구성 확인</a>
</p>
<p><small>고지: 편집자는 VDSina와 업무상 관계가 있으며, 이 파트너 링크를 통해 주문하면 사이트가 수수료를 받을 수 있습니다. VPS 사양은 실제 모니터링 데이터에 근거해 결정해야 합니다. 이 페이지는 VDSina가 위에서 설명한 모니터링 도구를 관리형 서비스로 제공한다고 주장하지 않습니다.</small></p>

## 여러 웹사이트를 두 수준에서 모니터링 {#monitor-multiple-websites-at-two-levels}

여러 사이트가 실행되는 VPS에서는 다음 두 수준을 감시하세요.

### 서버 수준 {#server-level}

- CPU/RAM/스왑;
- 디스크·inode·I/O;
- 데이터베이스;
- 네트워크;
- 핵심 서비스.

### 사이트 수준 {#site-level}

- 중요한 각 호스트 이름;
- TLS;
- 응답 시간;
- 5xx;
- 앱·작업 실패;
- 가능한 경우 사이트별 로그 또는 워커 부하.

서버 자체는 정상이어도 하나의 가상 호스트, 인증서 또는 웹사이트에는 장애가 발생할 수 있습니다.

사이트 통합과 장애 영역에 대한 판단은 [여러 웹사이트용 VPS]({{< relref "vps-for-multiple-websites.md" >}})를 참고하세요.

## VPS 모니터링 체크리스트 {#vps-monitoring-checklist}

| 지표 | 통과 기준 |
|---|---|
| 외부 가용성 | 중요한 호스트 이름을 VPS 외부에서 점검 |
| HTTP 상태 | 예상한 상태 코드·콘텐츠·상태 확인 엔드포인트 검증 |
| CPU | 지속 사용률·부하·프로세스별 사용 이력 보존 |
| RAM | 가용 메모리, 스왑 및 OOM 확인 가능 |
| 디스크 | 용량과 사용량 증가 추적 |
| Inode | inode 고갈 여부를 별도로 감시 |
| I/O | 스토리지가 중요할 때 지연 시간·I/O 대기 확인 가능 |
| 네트워크 | 처리량·오류·전송 경로 문제 징후를 관찰 가능 |
| 서비스 | 웹 서버·실행 환경·DB·워커 상태 감시 |
| 데이터베이스 | 앱에 필요한 가용성·지연 시간·연결 상태 확인 가능 |
| 작업 | cron·큐·백그라운드 작업의 실패 또는 적체 확인 가능 |
| TLS/DNS | 만료·이름 해석 오류 감지 가능 |
| 백업 | 마지막 성공 시점과 백업 작업 실패 감시 |
| 로그 | 사고 원인 연관 분석에 필요한 웹·앱·DB·시스템 로그 보유 |
| 알림 | 경고·위험 및 지속 시간·디바운스 규칙 설정 |
| 통지 | 중요한 알림이 VPS 장애 영역 외부로 전달 |
| 담당자 | 지정된 대응 담당자와 최초 조치 절차서 |
| 이력 보존 | 추세·근본 원인 분석에 충분한 지표·로그 이력 |
| 보안 | 모니터링 엔드포인트·대시보드가 의도치 않게 공개되지 않음 |
| 용량 계획 | 추세를 다음 최적화·확장 결정에 활용 |

## 기술 참고 자료 {#technical-references}

- Prometheus — Node Exporter를 이용한 Linux 호스트 지표 모니터링
- Prometheus — Alertmanager
- Uptime Kuma — 공식 프로젝트
- [VPS 백업 전략]({{< relref "vps-backup-strategy.md" >}})
- [VPS 보안 점검표]({{< relref "vps-security-checklist.md" >}})

## FAQ {#faq}

### VPS에서 무엇을 모니터링해야 하나요? {#what-should-i-monitor-on-a-vps}

최소한 외부 웹사이트 가용성, CPU, 사용 가능한 RAM·스왑·OOM, 디스크 용량, inode, 핵심 서비스, 애플리케이션 상태, TLS 만료일, 최근 백업 상태와 알림 전달 여부를 감시하세요.

### CPU 사용률이 80%를 넘으면 항상 문제인가요? {#is-cpu-over-80-always-bad}

아닙니다. CPU 사용률이 잠시 높아지는 것은 정상일 수 있습니다. 지속적인 사용률과 함께 부하, 요청 지연 시간, 큐 적체 및 실제 CPU를 사용하는 프로세스를 조사해야 합니다.

### Linux RAM은 왜 거의 가득 차 있나요? {#why-is-linux-ram-almost-full}

Linux는 남는 메모리를 캐시로 사용합니다. 사용률만 보고 경고하기보다 가용 메모리, 스왑 활동, OOM 발생 기록과 프로세스 메모리 증가를 감시하세요.

### 디스크 문제를 찾으려면 무엇을 확인해야 하나요? {#what-should-i-monitor-for-disk-problems}

파일시스템 용량, inode 사용량, 저장 공간 증가와 I/O 지연·대기 시간을 확인하세요. 남은 GB만으로 모든 디스크 장애 유형을 파악할 수는 없습니다.

### 가용성 모니터링에 ping만으로 충분한가요? {#is-ping-enough-for-uptime-monitoring}

아닙니다. 웹사이트, 데이터베이스 또는 TLS 경로에 장애가 있어도 ping은 성공할 수 있습니다. 사용자에게 보이는 상태는 HTTP(S)와 애플리케이션·서비스 점검으로 확인하세요.

### 가용성 감시 도구를 같은 VPS에서 실행해야 하나요? {#should-the-uptime-monitor-run-on-the-same-vps}

유일한 감시 도구를 같은 VPS에 두면 안 됩니다. VPS 전체나 네트워크 장애 시 감시 도구도 웹사이트와 함께 중단될 수 있습니다. 적어도 핵심 가용성 점검·알림 경로는 해당 장애 영역 밖에 두세요.

### 어떤 VPS 모니터링 도구가 가장 좋은가요? {#which-vps-monitoring-tool-is-best}

모든 환경에 가장 좋은 단일 도구는 없습니다. VPS 한 대에는 외부 가용성 점검과 가벼운 서버 지표 에이전트만 필요할 수 있습니다. 여러 서버에는 Prometheus, Grafana와 Alertmanager가 적합할 수 있습니다. 필요한 관측 범위, 이력 보존과 운영 복잡도를 기준으로 선택하세요.

### VPS 한 대에도 Prometheus와 Grafana가 필요한가요? {#do-i-need-prometheus-and-grafana-for-one-vps}

반드시 그렇지는 않습니다. 장기 지표, 맞춤형 쿼리와 여러 서버를 관리할 때 강력하지만 작은 환경에서는 가벼운 에이전트와 외부 가용성 점검으로 충분할 수 있습니다.

### 백업은 어떻게 모니터링하나요? {#how-should-i-monitor-backups}

작업 실패와 마지막 성공 백업의 경과 시간이 RPO를 초과하는 상황에 알림을 설정하세요. 실제 복원 가능성은 별도의 복원 테스트로 확인해야 합니다.

### 언제 VPS 업그레이드를 고려해야 하나요? {#when-should-monitoring-trigger-a-vps-upgrade}

최적화된 정상 워크로드가 CPU, RAM, 스토리지·I/O 또는 다른 자원을 반복적으로 소진한다는 과거 지표가 있을 때입니다. 일회성 급증은 업그레이드의 충분한 근거가 아닙니다.
