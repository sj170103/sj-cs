
    # 사고 분석 보고서

    ## 사고 개요
    - 사고 발생 시간: 2023-08-27
    - 사고 위치: 로켓 시스템 (Oxygen Tank)

    ## 폭발 전 로그
    ```txt
    2023-08-27 11:20:00,INFO,Heat shield performing as expected during reentry.
2023-08-27 11:25:00,INFO,Main parachutes deployed. Rocket descent rate reducing.
2023-08-27 11:28:00,INFO,Touchdown confirmed. Rocket safely landed.
2023-08-27 11:30:00,INFO,Mission completed successfully. Recovery team dispatched.
2023-08-27 11:35:00,INFO,Oxygen tank unstable.

    ```

    ## 폭발 로그
    ```txt
    2023-08-27 11:40:00,INFO,Oxygen tank explosion.

    ```

    ## 폭발 후 로그
    ```txt
    2023-08-27 12:00:00,INFO,Center and mission control systems powered down.

    ```

    ## 사고 원인 분석
    - 로그에 따르면, 'Oxygen tank explosion'은 {accident_time}에 발생한 것으로 보이며, 그 직전까지 정상적인 운영이 이루어졌습니다.
    - 사고의 근본 원인으로는 산소 탱크의 불안정성 문제가 발생했음을 알 수 있습니다.
    