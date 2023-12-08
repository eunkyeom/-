## 오목 강화학습
강화학습의 기초 기말 과제를 위한 프로젝트 입니다.

## 업데이트 중
(231130) 파이썬으로 구현한 오목게임에 강화학습 agent를 추가했습니다.
(231207) create_and_train_gibo.py 추가

## 파일 설명
main.py
 - 게임의 실행 및 종료

rule.py
 - 오목 룰 함수로 저장
 - 현재 위치를 기준으로 양방향으로 이동하며 연속된 돌의 개수 확인 (돌이 5개면 승리)

draw.py
 - 오목판 ui (15*15)

agent.py
 - 큐러닝으로 강화학습 수행하는 파이썬 파일

create_and_train_gibo.py
 - 기보 데이터를 직접 만들고 해당 데이터를 학습시킴
 - 게임이 끝난 후 현재의 게임 상태를 game_states에 추가
 - 학습을 위해 수집한 게임 상태들을 사용하여 에이전트 업데이트
