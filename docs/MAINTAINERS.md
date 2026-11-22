# 배포 담당자

학생에게는 ZIP과 START-HERE의 문장만 전달합니다. 다음 명령은 유지보수자용이며
Python 3.11 이상, 표준 라이브러리만 사용합니다.

`CI-EXAMPLE.yml`은 Windows·Mac·Linux 패키지 검사 워크플로 예시입니다.
GitHub Actions를 사용하려면 저장소 관리자가 워크플로 쓰기 권한으로
`.github/workflows/validate.yml`에 설치합니다. 현재 배포는 CI 실행을 주장하지 않습니다.

```text
python tools/verify.py
python -m unittest discover -s tests -v
python tools/build_release.py
```

ZIP 생성은 `bundle-manifest.json`에 명시된 검증된 파일만 포함합니다. 학생 연구,
개인 맥락, 테스트 산출물, .git, 인증 파일, 데이터베이스를 자동 수집하지 않습니다.
프로젝트 폴더 전체를 직접 압축해 재배포하지 마세요.

변경 후에는 검토를 마친 배포 파일 목록과 해시를 `tools/refresh_manifest.py`로
갱신합니다. 이 명령은 upstream 해시를 재승인하지 않습니다. 방법 변경 시에는
원본 비교·변경 고지·행동 검증도 함께 필요합니다.

새 버전은 `VERSION`과 VALIDATION을 갱신하고 Windows·Mac의 실제 앱 새 프로젝트에서
최소한 두 역할과 저장 결과를 확인합니다. 단위 테스트는 런타임 역할 등록을 증명하지
않습니다. 실행되지 않은 OS/역할/외부 데이터는 검증 완료로 표시하지 마세요.

원본 전체 실행 시스템이 필요하면 원본을 별도로 유지보수해야 합니다. 이 프로젝트에
실행 권한이나 MCP를 추가하는 것은 설치 개선이 아니라 제품 경계 변경입니다.
