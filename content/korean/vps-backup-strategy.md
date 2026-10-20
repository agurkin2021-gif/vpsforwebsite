---
title: "VPS 백업 전략"
slug: "vps-백업-전략"
draft: true
description: "VPS 백업 전략: RPO와 RTO를 정의하고 제공업체 백업 이미지와 독립적인 외부 백업을 결합하며, 데이터베이스와 비밀 정보를 보호하고 보존 정책과 실제 복원 테스트로 복구 가능성을 확인합니다."
image: "images/home/vps-for-website-hero.webp"
---

VPS 백업 전략은 단순히 “하루에 한 번 스냅샷을 켜는 것”이 아닙니다. 실제로 사용할 수 있는 복구 계획은 **허용 가능한 데이터 손실량(RPO), 복구에 걸릴 수 있는 시간(RTO), 반드시 보존해야 하는 데이터, 독립된 사본의 보관 장소, 백업 버전의 보존 기간, 실제로 복원을 수행해 봤는지**를 정의해야 합니다.

견고한 VPS 복구 계획은 대체로 제공업체 측의 빠른 복구 방법, 서버 외부의 독립적인 사본, 애플리케이션에 맞는 데이터베이스 백업을 결합합니다. 적절한 구성은 데이터가 얼마나 빨리 변하는지, 서비스 중단 비용이 얼마나 큰지에 따라 달라집니다.

백업 전략에는 담당자도 명확히 지정해야 합니다. 작업 실패, 복원 테스트, 복구 결정을 책임질 사람이 없다면 운영 방식부터 정하세요. [관리형 VPS와 비관리형 VPS]({{< relref "managed-vs-unmanaged-vps.md" >}})를 참고하세요.

서버 선택의 전반적인 기준은 [웹사이트용 VPS 호스팅]({{< relref "_index.md" >}})을 참고하세요.

[핵심 요약](#quick-answer) · [진단 도구](#vps-backup-strategy-checker) · [RPO / RTO](#start-with-rpo-and-rto) · [백업 계층](#snapshot-image-file-backup-and-replication-are-different) · [3-2-1](#a-practical-3-2-1-model-for-vps) · [복원 테스트](#test-restores-and-measure-real-rto) · [VDSina](#how-vdsina-backups-fit-the-strategy) · [FAQ](#faq)

## 핵심 요약 {#quick-answer}

실용적인 VPS 복구 구조는 여러 계층으로 구성됩니다.

| 계층 | 주요 역할 | 이것만으로 보장하지 못하는 사항 |
|---|---|---|
| **제공업체 백업 이미지 / 스냅샷** | 서버 전체를 빠르게 이전 상태로 되돌리거나 재구축 | 제공업체 계정 또는 저장소를 사용할 수 없을 때의 독립적인 복구 |
| **데이터베이스 일관성을 보장하는 백업** | 애플리케이션 상태와 최근 변경 데이터를 복원 | 서버 전체 설정의 복원 |
| **파일 / 설정 백업** | 업로드, 설정, 앱 데이터 및 선택한 파일 복원 | 서버 전체를 신속하게 복구하는 능력 |
| **독립적인 외부 사본** | 주 제공업체, 계정 또는 서버 장애에도 데이터 보존 | 복원을 연습하지 않았다면 짧은 RTO 달성 |
| **복원 훈련** | 사본, 복구 키와 실행 절차가 실제로 작동함을 입증 | 지속적인 감시가 없다면 이후 백업도 계속 성공한다는 보장 |

일반적인 웹사이트 VPS 배포에서는 다음 구성을 기본으로 삼을 수 있습니다.

- 빠른 롤백을 위한 제공업체 측 이미지 또는 스냅샷;
- 파일, 설정과 데이터베이스를 다른 장애 영역으로 보내는 암호화된 독립 백업;
- 여러 복구 지점;
- 허용 가능한 데이터 손실량에 맞춘 데이터베이스 백업 주기;
- 정기적인 복원 테스트.

단 하나의 “백업 성공” 상태에 의존하는 것보다 훨씬 유용합니다.

## VPS 백업 전략 진단 {#vps-backup-strategy-checker}

이 진단 도구는 필요한 복구 구조를 판단하는 데 도움을 줍니다. 복구 성공을 보장하지는 않습니다.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-backup-strategy-checker-form">
  <div class="mb-6">
    <label for="bk-workload" class="form-label">작업 부하 유형</label>
    <select id="bk-workload" class="form-input">
      <option value="static">정적 / 소개용 / 변경이 드문 사이트</option>
      <option value="cms">워드프레스 / CMS / 비즈니스 웹사이트</option>
      <option value="transactional">우커머스 / 주문 / 회원 관리 / 잦은 데이터 쓰기</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rpo" class="form-label">허용 가능한 최대 데이터 손실량(RPO)</label>
    <select id="bk-rpo" class="form-input">
      <option value="24">최대 24시간</option>
      <option value="4">최대 4시간</option>
      <option value="1">최대 1시간</option>
      <option value="lt1">1시간 미만</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rto" class="form-label">허용 가능한 최대 서비스 중단 시간(RTO)</label>
    <select id="bk-rto" class="form-input">
      <option value="24">최대 24시간</option>
      <option value="4">최대 4시간</option>
      <option value="1">약 1시간</option>
      <option value="lt1">1시간 미만</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-offsite" class="form-label">서버 외부에 독립적인 백업 사본이 있습니까?</label>
    <select id="bk-offsite" class="form-input"><option value="no">아니요</option><option value="yes">예</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-db" class="form-label">데이터베이스 일관성을 보장하는 백업 방법을 검증했습니까?</label>
    <select id="bk-db" class="form-input">
      <option value="na">해당 없음 / 데이터베이스 없음</option>
      <option value="no">아니요 / 확인하지 않음</option>
      <option value="yes">예</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-restore" class="form-label">최근 복원 테스트를 성공적으로 완료했습니까?</label>
    <select id="bk-restore" class="form-input"><option value="no">아니요</option><option value="yes">예</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-creds" class="form-label">백업 자격 증명과 암호화 복구 키를 VPS와 분리해 보관합니까?</label>
    <select id="bk-creds" class="form-input"><option value="no">아니요 / 확인하지 않음</option><option value="yes">예</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-versions" class="form-label">복구 지점 여러 개와 보존 이력이 있습니까?</label>
    <select id="bk-versions" class="form-input"><option value="no">최신 사본 하나만 / 확인하지 않음</option><option value="yes">예</option></select>
  </div>
  <button class="btn btn-primary" type="submit">백업 전략 확인</button>
</form>
<p id="vps-backup-strategy-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">실제로 필요한 복구 요건을 선택하세요.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-backup-strategy-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var workload = val("bk-workload");
    var rpo = val("bk-rpo");
    var rto = val("bk-rto");
    var offsite = val("bk-offsite") === "yes";
    var db = val("bk-db");
    var restore = val("bk-restore") === "yes";
    var creds = val("bk-creds") === "yes";
    var versions = val("bk-versions") === "yes";

    var criticalGap = !offsite || !restore || !creds || !versions || (db === "no");
    var result;

    if (criticalGap) {
      result = "중대한 백업 결함: 복구 전략이 아직 검증되지 않았거나 독립적이지 않은 복구 경로에 의존하고 있습니다. 독립적인 외부 사본과 여러 복구 지점, 별도로 보관하는 복구 자격 증명 및 키, 필요한 데이터베이스 일관성 백업과 실제 복원 테스트를 마련하세요.";
    } else if (rto === "lt1" || rto === "1") {
      result = "짧은 RTO / 재해 복구 구조 재검토: 백업 자체가 올바르더라도 수동 재구축으로는 1시간 복구 목표를 지키지 못할 수 있습니다. 전체 복구 시간을 측정하고, 실제 RTO가 너무 길면 자동화, 사전 구축 이미지, 대기 서버 또는 작업 부하 분리를 검토하세요.";
    } else if (workload === "transactional" || rpo === "lt1" || rpo === "1") {
      result = "거래 처리 / 빈번한 DB 백업: 독립적인 복구 계층을 유지하면서 필요한 RPO를 충족하도록 데이터베이스 보호 주기를 정하세요. 하루 한 번의 백업으로는 1시간 데이터 손실 목표를 달성할 수 없습니다.";
    } else {
      result = "기본 복구 전략: 핵심 계층이 갖춰져 있습니다. 제공업체 복구 지점과 독립적인 외부 백업을 유지하고, 작업 실패를 감시하며, 여러 버전을 보존하고 실제 시간을 측정하는 복원 훈련을 반복하세요.";
    }

    document.getElementById("vps-backup-strategy-result").textContent = result;
  });
});
</script>

## RPO와 RTO부터 정의 {#start-with-rpo-and-rto}

전략을 결정하는 핵심 숫자는 두 가지입니다.

### 복구 시점 목표 — RPO {#recovery-point-objective--rpo}

RPO는 다음 질문에 답합니다.

**비즈니스가 최근 데이터 중 얼마나 잃어도 감당할 수 있습니까?**

RPO가 다음과 같다면:

- **24시간** — 하루에 한 번 성공적으로 생성한 복구 지점이 허용될 수 있습니다;
- **4시간** — 일일 백업만으로는 부족합니다;
- **1시간** — 변경되는 애플리케이션과 데이터베이스 상태를 최소한 그 주기로 보호해야 합니다;
- **수분 단위** — 일반적인 예약 백업만으로 충분하지 않을 수 있습니다.

RPO는 서비스 중단 시간이 아니라 **데이터 손실량**에 관한 지표입니다.

### 복구 시간 목표 — RTO {#recovery-time-objective--rto}

RTO는 다음 질문에 답합니다.

**웹사이트나 서비스를 얼마나 오랫동안 사용할 수 없어도 됩니까?**

백업이 RPO를 충족하더라도 RTO를 충족하지 못할 수 있습니다.

예를 들면 다음과 같습니다.

- 데이터베이스를 매시간 복사합니다;
- 최근 데이터의 손실량은 1시간 미만입니다;
- 그러나 VPS를 다시 만들고 데이터를 내려받아 DB를 복원하고 사이트를 검증하는 데 6시간이 걸립니다.

이 전략은 1시간 RPO를 충족할 수 있지만 실제 RTO는 약 6시간입니다.

NIST의 비상 계획 지침은 RPO를 복구 기준 시점으로, RTO를 허용 가능한 최대 서비스 중단 시간으로 정의합니다. 도구를 선택하기 전에 이 목표부터 정하세요.

## 무엇을 백업해야 하나요? {#what-should-be-backed-up}

서버의 구성 요소를 **재구축 가능한 항목**과 **상태가 있거나 다시 만들기 어려운 항목**으로 구분하세요.

### 재구축 가능한 항목 {#rebuildable}

코드나 자동화로 다시 만들 수 있는 경우가 많습니다.

- 기본 운영체제;
- 패키지;
- 이미 Git에 안전하게 보관된 애플리케이션 코드;
- 다시 빌드하거나 내려받을 수 있는 컨테이너 이미지;
- 표준 웹 서버 패키지.

### 상태가 있거나 복원이 어려운 항목 {#stateful--difficult-to-recreate}

일반적으로 우선순위가 더 높습니다.

- 데이터베이스;
- 사용자 업로드와 미디어;
- 같은 서버에서 운영하는 경우 메일함;
- 설정;
- 복구에 필요한 환경 변수와 비밀 정보;
- 다시 발급하거나 교체하기 어려운 TLS 인증서와 개인 키;
- 애플리케이션이 생성한 데이터;
- 컨트롤 패널과 사이트 설정;
- cron과 워커 설정;
- DNS를 VPS에서 운영한다면 DNS 영역 데이터;
- 다른 곳에 저장되지 않은 맞춤형 스크립트.

데이터베이스나 사이트를 다시 시작하는 데 필요한 비밀 정보를 빠뜨리면서 캐시, 임시 파일, 쉽게 재생성할 수 있는 결과물을 무작정 복사하는 데 백업 공간을 낭비하지 마세요.

## 스냅샷, 이미지, 파일 백업과 복제는 서로 다릅니다 {#snapshot-image-file-backup-and-replication-are-different}

서로 같은 수단으로 취급하지 마세요.

### 제공업체 스냅샷 / 서버 이미지 {#provider-snapshot--server-image}

다음 상황에 유용합니다.

- 위험이 있는 업데이트 후 빠른 롤백;
- 서버 전체 복구;
- 가상 머신 복제 또는 재생성.

한계:

- 제공업체나 계정과 동일한 장애 영역에 있을 수 있습니다;
- 개별 파일 또는 사이트 단위 복원이 어려울 수 있습니다;
- 애플리케이션과 데이터베이스의 일관성을 별도로 이해해야 합니다;
- 최신 이미지 하나만 있으면 이전 시점의 기록이 부족합니다.

### 파일 단위 백업 {#file-level-backup}

다음 항목에 유용합니다.

- 업로드 파일;
- 설정;
- 선택한 애플리케이션 데이터;
- 세부 항목별 복원.

restic이나 Borg 같은 도구를 사용하면 원격 저장소에 암호화된 여러 버전의 백업을 보관할 수 있습니다.

### 데이터베이스 백업 {#database-backup}

데이터베이스 엔진에 맞는 방법을 사용하세요.

- 논리적 덤프;
- 데이터베이스 자체 백업 도구;
- 애플리케이션 일관성을 유지하는 스냅샷 또는 절차.

실행 중인 데이터베이스 파일을 그대로 복사한다고 해서 사용 가능한 DB 백업이 만들어진다고 가정하지 마세요.

### 복제 / 대기 서버 {#replication--standby}

복제는 복구 시간이나 데이터 손실을 줄일 수 있지만, 그 자체로 과거 시점의 백업은 아닙니다.

잘못된 삭제, 손상 또는 애플리케이션 오류까지 함께 복제될 수 있습니다.

필요한 경우 가용성과 RTO를 위해 복제 및 대기 서버를 사용하되, 과거 시점으로 복구할 수 있도록 버전별 백업도 유지하세요.

## VPS에 적용하는 실용적인 3-2-1 모델 {#a-practical-3-2-1-model-for-vps}

일반적인 3-2-1 모델은 다음을 뜻합니다.

- 중요한 데이터의 사본 **3개**;
- **2가지 서로 다른 저장 방식 또는 장애 영역**;
- **1개는 외부, 즉 주 장애 영역 밖에 보관**.

VPS에서는 다음과 같이 적용할 수 있습니다.

1. VPS의 실제 운영 데이터;
2. 빠른 복구를 위한 제공업체 백업 이미지;
3. 독립적인 장소에 보관하는 암호화된 외부 파일 및 데이터베이스 백업.

목표는 구호의 숫자를 기계적으로 맞추는 것이 아닙니다. 한 번의 사고로 운영 데이터와 모든 복구 사본이 동시에 사라지는 일을 막는 것입니다.

장애 영역의 예시는 다음과 같습니다.

- VPS 파일 시스템;
- 제공업체의 백업 저장소;
- 제공업체 계정;
- 별도의 객체 저장소 계정 또는 제공업체;
- 오프라인 사본 또는 변경할 수 없도록 보호된 사본.

VPS를 장악한 공격자가 같은 자격 증명으로 모든 백업을 삭제할 수 있다면, 사본이 실질적으로 독립되어 있다고 볼 수 없습니다.

## 데이터베이스 일관성을 보장하는 백업 {#database-consistent-backups}

사이트가 실행되는 동안에도 데이터베이스 상태는 계속 변합니다.

올바른 전략이라면 DB 엔진을 어떤 방식으로 보호하는지 알아야 합니다.

워드프레스, MySQL 또는 MariaDB에서는 다음 방법을 사용할 수 있습니다.

- 논리적 덤프;
- DB 전용 백업 도구;
- 서로 맞춰 수행하는 스냅샷;
- 데이터베이스 일관성을 명시적으로 처리하는 백업 소프트웨어.

PostgreSQL에서는 필요한 RPO에 따라 PostgreSQL에 맞는 백업과 시점 복구(PITR) 방법을 사용하세요.

중요한 것은 특정 도구가 아니라 복원된 DB의 내부 상태가 일관되고 실제로 사용할 수 있어야 한다는 점입니다.

워드프레스의 애플리케이션 상태와 운영에 대해서는 [워드프레스용 VPS]({{< relref "vps-for-wordpress.md" >}})를 참고하세요.

다음을 테스트하세요.

- 덤프 또는 백업 작업이 완료됩니다;
- 백업 파일이 비어 있지 않습니다;
- 복원 또는 가져오기가 성공합니다;
- 대표적인 테이블과 레코드가 존재합니다;
- 애플리케이션이 접속하여 중요한 데이터 읽기와 쓰기를 수행합니다.

## 거래가 발생하는 사이트는 다른 RPO가 필요합니다 {#transactional-sites-need-a-different-rpo}

단순한 소개 사이트는 하루 전 사본으로도 충분할 수 있습니다.

반면 거래가 발생하는 쇼핑몰은 그렇지 않을 수 있습니다.

WooCommerce, 회원 관리, 청구 또는 주문 시스템에서는 최근에 변경된 상태를 얼마나 잃을 수 있는지 정하세요.

- 주문;
- 결제;
- 재고;
- 고객;
- 회원 자격;
- 양식 제출;
- 업로드.

매시간 주문이 들어오는 쇼핑몰에서는 하루에 한 번의 DB 백업으로 많은 거래 기록을 잃을 수 있습니다.

쇼핑몰 작업 부하는 [우커머스용 VPS]({{< relref "vps-for-woocommerce.md" >}})를 참고하세요. 이 페이지의 백업 주기는 허용 가능한 거래 데이터 손실 시간에 맞춰 정해야 합니다.

## 백업 빈도와 보존 기간 {#backup-frequency-and-retention}

각 데이터 유형의 백업 주기는 해당 RPO보다 느려서는 안 됩니다.

데이터에 따라 다른 일정이 필요할 수 있습니다.

- DB: 빈번하게;
- 업로드: 빈번하게 또는 이벤트 발생 시;
- OS 및 설정: 중요한 변경 후와 정기 일정에 따라;
- 제공업체의 전체 이미지: 상대적으로 드물게, 특히 위험한 변경 전후에 유용.

보존 정책은 문제가 늦게 발견되더라도 복구할 수 있도록 해 줍니다.

예를 들면 다음 사본을 유지하는 방식이 있습니다.

- 최근의 시간별 복구 지점;
- 여러 개의 일별 사본;
- 여러 개의 주별 사본;
- 일부 월별 사본.

정확한 보존 기간은 다음을 기준으로 정하세요.

- 비즈니스의 복구 필요;
- 저장 비용;
- 데이터 변경 속도;
- 규정 준수와 법적 요구사항;
- 손상이나 침해가 발견되지 않은 채 지속될 수 있는 시간.

“최신 버전” 하나만 보관하지 마세요.

## Keep an independent off-server destination

A backup on the same VPS disk does not protect against:

- disk/filesystem loss;
- server deletion;
- root compromise;
- ransomware;
- account mistake;
- provider-side loss of that VM.

Move or stream recovery data outside the VPS.

Possible destinations:

- object storage;
- another backup service/provider;
- another VPS used only for backups;
- offline/controlled storage.

Separate provider/account credentials where practical.

## Encrypt backups — and protect the recovery key

Encrypt sensitive backup data in transit and at rest where appropriate.

But encryption creates another recovery dependency.

Do not store the **only** backup password/key:

- only on the VPS;
- only in the same password vault/account that might be unavailable;
- only inside the encrypted backup itself.

Keep recovery credentials/keys in a secure independent location and include key availability in restore drills.

## Separate backup credentials and deletion rights

A production-server compromise should not automatically give an attacker permission to erase every recovery copy.

Prefer:

- scoped backup credentials;
- write access without broad delete privileges where the storage supports it;
- separate administrative credentials;
- retention lock/immutability where appropriate;
- offline/air-gapped copy for high-value data.

The exact design depends on the storage service.

This is one reason backups are also a security control; see [VPS Security Checklist]({{< relref "vps-security-checklist.md" >}}).

## Monitor backup jobs

Automation reduces forgotten backups, but failed automation can fail silently.

Monitor:

- last successful backup time;
- failed/partial jobs;
- repository/storage availability;
- credential expiry;
- free disk before local staging;
- offsite storage quota;
- DB dump failures;
- backup duration changes;
- unusually small backup size;
- retention/prune failures.

A green cron/service status proves the command ran. It does not prove the restore works.

Broader server/service alert design belongs to [VPS Monitoring]({{< relref "vps-monitoring.md" >}}); backup-job health remains part of the recovery strategy itself.

## Test restores and measure real RTO

A backup becomes credible when it restores.

Run recovery drills into an isolated clean destination.

Test enough of the full sequence:

1. provision a fresh VPS/test environment;
2. retrieve the correct backup point;
3. retrieve encryption/repository credentials;
4. restore files/configuration;
5. restore/import the database;
6. restore required secrets/certificates;
7. configure services/networking;
8. start the application;
9. test important pages and transactions;
10. verify background jobs/integrations;
11. measure elapsed recovery time.

Record the measured result.

If the business RTO is four hours and the test takes eight, the backup strategy has failed the business requirement even if every file restored successfully.

NIST guidance emphasizes regular backup creation, restoration testing and recovery exercises.

## Restore granularity matters

A good strategy supports the failure you actually have.

### Single-file/site recovery

Needed for:

- deleted upload;
- broken config;
- one compromised site;
- one bad database/table recovery.

### Full-server recovery

Needed for:

- dead/deleted VPS;
- filesystem failure;
- severe compromise;
- provider/server replacement.

If the only backup is a full disk image, restoring one file may be inconvenient.

If the only backup is selected files, rebuilding the complete VPS may take too long.

Layer the methods.

## Multiple websites need site-level restore

On a multi-site VPS, do not design recovery so that fixing Site A automatically rolls Site B/C/D back to yesterday.

Prefer backups that let you restore:

- one document root;
- one database;
- one panel/user;
- one set of uploads;
- the full VPS only when required.

For the architecture/failure-domain decision, see [VPS for Multiple Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Backups can cause outages too

Backup work consumes resources.

Potential impact:

- DB dump CPU;
- compression CPU;
- read I/O;
- temporary disk usage;
- object-storage upload bandwidth;
- cache eviction;
- backup overlap with imports/scans/traffic peaks.

Avoid building a 30 GB local archive when the VPS has only 10 GB free.

Where practical:

- stream backups directly off-server;
- monitor temporary disk usage;
- schedule heavy backup work outside traffic peaks;
- rate-limit where the tool supports it;
- measure backup duration.

## How VDSina backups fit the strategy

VDSina's public documentation currently describes several useful recovery functions:

- manual server backup copies;
- scheduled backups;
- restore a backup to the server it came from;
- create a new server from a backup;
- clone a server;
- download a backup image.

The download documentation shows a backup filename in the form:

`vXXX.backup.hosted-by-vdsina.com.img.gz`

That downloadable image is a useful portability layer because a recovery copy does not have to remain only inside the provider panel.

However:

- treat the provider image as **one layer**, not the entire strategy;
- test how your chosen recovery environment uses the downloaded image;
- do not assume every hypervisor can consume it directly without conversion;
- keep application/file/database backups for granular recovery;
- keep an independent failure-domain copy where the risk justifies it.

VDSina's own Terms explicitly state that the customer is responsible for backups and recommends a routine backup process plus periodic restore testing.

When creating a new VDSina server from a provider backup, their QA notes that the backup/new server must meet provider constraints such as data-center placement and sufficient disk quota; network settings may also require adjustment after restoration.

Do not confuse backup with migration. A backup can be part of a migration safety net, but live cutover, final writes, DNS and rollback are separate concerns; see [Website migration to VPS]({{< relref "website-migration-to-vps.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current VPS backup options</a>
</p>
<p><small>Disclosure: the editor has a professional relationship with VDSina, and this site may earn a commission if you order through this partner link. Provider backup features do not replace an independent recovery strategy or restore testing.</small></p>

## Recovery runbook

Write down the recovery process before the outage.

At minimum record:

- backup destinations;
- restore-point naming/retention;
- repository credentials;
- encryption-key recovery location;
- which data is DB/files/config;
- fresh-server provisioning steps;
- software/runtime versions;
- restore order;
- DNS/network steps;
- external integrations/webhooks;
- acceptance tests;
- who makes the recovery/rollback decision.

Keep the runbook somewhere available even when the VPS itself is unavailable.

## VPS backup checklist

| Control | Pass condition |
|---|---|
| RPO | maximum acceptable data-loss window defined |
| RTO | maximum acceptable downtime defined |
| Data inventory | DB, uploads, config, secrets and other state classified |
| Provider recovery | image/snapshot schedule understood |
| Database | engine-aware, restorable DB backup method |
| Offsite copy | independent recovery copy outside VPS failure domain |
| Credentials | backup account scoped/separated from production |
| Encryption | sensitive backups encrypted where appropriate |
| Key recovery | recovery key/password stored outside failed VPS |
| Retention | multiple historical restore points |
| Monitoring | failed/partial/stale backup jobs detected |
| Disk/I/O | backup process cannot silently fill/overload production |
| Granularity | file/site/DB restore possible where needed |
| Full recovery | complete VPS/service rebuild path exists |
| Restore test | isolated restore completed successfully |
| Measured RTO | actual recovery duration recorded and within target |
| Runbook | recovery order, credentials, DNS and acceptance tests documented |
| Owner | named person/team owns backup and restore work |

## Technical references

- NIST SP 800-34 Rev.1 — RPO/RTO and contingency planning
- NIST SP 1339 — backup creation, testing and recovery exercises
- Ubuntu — restic backup/restore tool
- Ubuntu — BorgBackup
- VDSina Terms — customer backup responsibility
- VDSina — server backup / restore / new server from backup
- VDSina — scheduled backups
- VDSina — download and use a server backup

## FAQ

### What is a good VPS backup strategy?

Define RPO/RTO, keep independent recovery copies, protect databases with an application-consistent method, retain multiple versions, monitor failed jobs and regularly restore into a clean test environment.

### Is a VPS snapshot enough?

Not as the only recovery layer. A provider snapshot/image is useful for fast rollback and full-server recovery, but it may share the same provider/account failure domain and is less convenient for granular restores.

### What does 3-2-1 mean for a VPS?

Keep the live data plus multiple recovery copies using independent storage/failure domains, with at least one copy outside the primary VPS/provider failure path.

### How often should I back up a VPS?

Choose frequency from the RPO of each data type. A static site may tolerate daily copies; a transactional database may require hourly or more frequent protection.

### What is the difference between RPO and RTO?

RPO is the maximum acceptable recent data loss. RTO is the maximum acceptable downtime until the service is restored.

### Should I back up the whole VPS or only website files?

Usually both layers are useful. A server image speeds full recovery; file/database backups make granular and application-consistent restores easier.

### How do I back up MySQL or PostgreSQL safely?

Use an engine-aware logical/native backup or coordinated application-consistent method, then prove it by restoring/importing into an isolated test environment.

### Should backups be encrypted?

Sensitive recovery data should be encrypted where appropriate, but keep the recovery password/key safely outside the failed VPS.

### Is replication a backup?

Not by itself. Replication can copy accidental deletion, corruption or malicious changes. Keep historical/versioned backups in addition to replication/standby.

### Does VDSina provide VPS backups?

VDSina documents manual and scheduled backup copies, restore/create-server-from-backup functions and downloadable backup images. Their Terms still place backup responsibility on the customer and recommend periodic restore testing.

### How often should I test restores?

On a defined schedule and after meaningful backup/architecture changes. High-value or rapidly changing systems should be tested often enough that the measured recovery process remains trustworthy.

### What if my RTO is under one hour?

A backup-only design may be too slow. Time a full recovery drill and consider automation, prebuilt recovery images, warm standby or architecture changes if the measured RTO misses the target.
