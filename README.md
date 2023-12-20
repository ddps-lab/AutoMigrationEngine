# 마이그레이션 실험 자동화

프로세스 및 컨테이너 마이그레이션에서 발생하는 주요 이슈인 CPU 호환성을 실험함.

### Dir 구조

```data_processing_for_lscpu```: CPU feature set을 google spreadsheet에 write, grouping 등의 작업을 수행하며 실험 비용을 절감하기 위해 각 CPU feature 그룹을 minimize할 수 있음.  
```infrastructure```: 실험 인프라 생성 관련 terraform code.  
```ssh_scripts```: 실험이 이루어지는 인스턴스 제어 관련 ansible scripts.  
```ExternalMigration(all of cases).py```: 실험을 수행하는 메인 스크립트. 해당 스크립트만 실행하면 모든 실험이 자동으로 이루어짐.  
```ExternalMigration(re-experiment)```: 실험 중간에 누락이 발생하는 경우 자동으로 이를 탐지하여 재실험. S3에 로드되지 않은 실험 케이스를 파악하여 재실험함.  
```InternalMigration```: 그룹 내 마이그레이션 실험