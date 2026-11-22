# Hyperpass Agent Team

**Codex 앱에서 바로 여는 투자 리서치 팀.**

> 프리뷰 배포: 패키지·구조 검증은 완료했습니다. Windows와 Mac의 실제 앱에서
> 첫 사용 전체 흐름은 아직 검증 완료로 표시하지 않습니다. 먼저 소수 수강생과
> START-HERE의 동작 검사를 확인하세요. [검증 결과](docs/VALIDATION.md)

Head Manager와 9개 전문 역할이 질문에 맞춰 팀을 구성하고, 근거를 검토하며,
다음 분석에 활용할 보고서와 판단 이력을 프로젝트에 남깁니다.

## 수강생 시작 방법

1. [수강생용 ZIP 다운로드](https://github.com/rrw9002-ops/Hyperpass-Agent-Team/releases/download/v1.0.0-preview.1/Hyperpass-Agent-Team-1.0.0-preview.1.zip)를 새 폴더에 풉니다. GitHub에서는 **Code → Download ZIP**도 가능합니다.
2. Codex 앱에서 압축을 푼 프로젝트 폴더를 엽니다. `AGENTS.md`가 있는 폴더입니다.
3. 새 채팅에 [START-HERE.md](START-HERE.md)의 시작 문장을 붙여넣습니다.
4. 실제 역할 호출과 보고서 저장을 확인한 뒤, 분석하고 싶은 질문을 입력합니다.

Windows·Mac 공통입니다. 앱 로그인과 서브에이전트를 사용할 수 있는 환경이 필요하며,
기본 사용에는 터미널 명령, Git, Python, uv, API 키, 별도 서버 설치가 필요 없습니다.
Codex 사용 요금·한도는 사용하는 계정에 따릅니다. 최신 데이터 조회와 수치 계산은
앱에서 실제 사용할 수 있는 도구에 따라 달라집니다.

## 팀이 일하는 방식

질문 → Head Manager → 필요한 최소 전문 역할 → 근거 검수·채택 →
보완 요청 / 새 전문 역할 / 독립 검토 → 통합 판단·기록.

| 역할 | 담당 |
| --- | --- |
| Fundamental Analyst | 기업·사업·재무·회계 품질 |
| Technical Analyst | 가격·거래량·추세·변동성·유동성 |
| News Analyst | 공시·뉴스·사건 순서·내러티브 |
| Macro Analyst | 금리·환율·정책·경기와 전달 경로 |
| Instrument Analyst | ETF·지수·옵션·암호자산 구조 |
| Valuation Analyst | 가치평가·역산 기대·시나리오·민감도 |
| Portfolio Manager | 보유 맥락·편입 적합성·집중도·비중 검토 |
| Risk Manager | 독립 위험 검토·하방·한계·중단 조건 |
| Judgment Reviewer | 근거에서 결론으로 이어지는 논리의 독립 검토 |

간단한 질문은 메인이 직접 답합니다. 매번 9명을 모두 부르지 않습니다.
모든 역할은 앱에서 선택한 모델·추론 설정을 따릅니다.

## 원본과의 관계

[Hyperpass-Tradingagent](https://github.com/moneybuilderjay-cmyk/Hyperpass-Tradingagent)의
TradingCodex 2.1.3을 기준으로 팀의 연구 운영 규칙과 전문 분석 방법을 옮긴
**별도 연구 전용 배포본**입니다. 원본 코드를 덮어쓰거나 인증을 우회하지 않습니다.

보존: 9개 전문 역할, 동적 최소 팀, 병렬 독립 분석, 근거 채택, 피드백 루프,
독립 위험·판단 검토, 맥락 분리, 시점·출처·계산·반대 근거·복기 원칙.

변경: 서비스/MCP 기록을 파일 기록으로 교체하고 모델 고정을 제거했습니다.
서비스의 인증된 원장·강제 권한 경계·주문 기능·웹 뷰어는 제공하지 않습니다.
**프롬프트와 파일 해시는 원본의 보안·인증·실행 기능과 동등하지 않습니다.**
전체 원본 기능의 대체품이 필요한 경우 이 패키지를 그 용도로 사용하지 마세요.
[항목별 보존·차이](docs/PRESERVATION.md)와 [검증 범위](docs/VALIDATION.md)를 확인하세요.

## 자료와 사용 예시

- [처음 시작](START-HERE.md) / [설치 안내를 맡기는 프롬프트](prompts/SETUP.md)
- [실제 분석 질문 예시](prompts/EXAMPLES.md) / [문제 해결](docs/TROUBLESHOOTING.md)
- [원본·강의 연결](docs/COURSE-MAP.md) / [배포 담당자 안내](docs/MAINTAINERS.md)

기본 자료는 공개 출처 또는 사용자가 제공한 파일입니다. OpenBB·DART·TradingView·
Notion 등은 이미 연결되어 있을 때 선택적으로 사용합니다. 자료가 없으면 한계로
남기며 시세·재무 수치·백테스트 성과를 생성하지 않습니다.

학생의 연구 결과와 개인 맥락 폴더는 Git과 배포 ZIP에서 제외합니다.
라이선스는 Apache-2.0이며 원본 저작권과 변경 고지는 [NOTICE](NOTICE)에 있습니다.
