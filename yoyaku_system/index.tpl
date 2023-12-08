<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>席の予約システム</title>
    <style>
      .parent {
        display: flex;
      }
      .sun {
        padding: 10px 10px;
        margin: 10px;
        border: 4px solid #000;
        height: 370px;
        width: 1050px;
      }
      .senaka {
        padding: 20px 10px;
        margin: 0px 0px -20px -30px;
        border: 4px solid #000;
        display: block;
        cursor: pointer;
        border-radius: 10px;
        height: 40px;
        width: 1px;
      }
      .seat {
        padding: 20px 10px;
        margin: 0px 0px 0px 40px;
        border: 4px solid #000;
        font-size: 35px;
        text-indent: -5px;
        font-family: "arialblack", "sans-serif";
        display: block;
        cursor: pointer;
        border-radius: 9px;
        height: 40px;
        width: 60px;
      }
      .untenseki1 {
        padding: 20px 10px;
        margin: 0px 0px 0px 40px;
        display: block;;
        border-right: 6px double #000;
        border-top: 6px double #000;
        height: 40px;
        width: 60px;
      }
      .untenseki2 {
        padding: 20px 10px;
        margin: 0px 0px 0px 40px;
        display: block;
        border-right: 6px double #000;
        border-bottom: 6px double #000;
        height: 40px;
        width: 60px;
      }
      .noru {
        padding: 20px 10px;
        margin: 20px 0px 0px 40px;
        border: 4px double #000;
        display: block;
        height: 20px;
        width: 60px;
      }
      .kieru {
        pointer-events: none;
        opacity: 0;
      }

    /* ... その他のスタイル ... */
      .reserved{
        background-color: #A4C6FF;
        pointer-events: none;
        opacity: 0.5;
      }        
      .seat.selected {
        background-color: #5D99FF;
        pointer-events: auto;
        opacity: 1;
      }
    </style>
</head>
<body>
<div id="seats" class="sun">
    <div class="parent">
        <div class="untenseki1"></div>
        <div class="senaka kieru"></div>
        % for i in range(1, 8):
            % if i in yoyaku_seki:
                <div class="seat reserved">&nbsp;{{i}}</div>
                <div class="senaka reserved"></div>
            % else:
                <div class="seat" data-seat-number="{{i}}" onclick="reserveSeat({{i}})">&nbsp;{{i}}</div>
                <div class="senaka" onclick="reserveSeat({{i}})"></div>
            % end
        % end
    </div>
    <div class="parent">
        <div class="untenseki2"></div>
        <div class="senaka kieru"></div>
        % for i in range(8,15):
            % if i in yoyaku_seki:
                % if i < 10:
                    <div class="seat reserved">&nbsp;{{i}}</div>
                    <div class="senaka reserved"></div>
                % else:
                    <div class="seat reserved">{{i}}</div>
                    <div class="senaka reserved"></div>
                % end
            % else:
                % if i < 10:
                    <div class="seat" data-seat-number="{{i}}" onclick="reserveSeat({{i}})">&nbsp;{{i}}</div>
                    <div class="senaka" onclick="reserveSeat({{i}})"></div>
                % else:
                    <div class="seat" data-seat-number="{{i}}" onclick="reserveSeat({{i}})">{{i}}</div>
                    <div class="senaka" onclick="reserveSeat({{i}})"></div>
                % end
            % end
        % end
    </div>
    <div class="parent">
        % for i in range(1,8):
            <div class="seat kieru"></div>
            <div class="senaka kieru"></div>
        % end
        % if 15 in yoyaku_seki:
            <div class="seat reserved">&nbsp;15</div>
            <div class="senaka reserved"></div>
        % else:
            <div class="seat" data-seat-number=15 onclick="reserveSeat(15)">15</div>
            <div class="senaka" onclick="reserveSeat(15)"></div>
        % end
    </div>
    <div class="parent">
        % for i in range(16,23):
            % if i==18:
                <div class="noru">搭乗口</div>
            % end
                
            % if i in yoyaku_seki:
                <div class="seat reserved">{{i}}</div>
                <div class="senaka reserved"></div>
            % else:
                <div class="seat" data-seat-number="{{i}}" onclick="reserveSeat({{i}})">{{i}}</div>
                <div class="senaka" onclick="reserveSeat({{i}})"></div>
            % end
        % end
    </div>
</div>

<button onclick="confirmReservation()">予約決定</button>

<script>
    let selectedSeatNumber = null;

    function reserveSeat(seatNumber) {
        if (selectedSeatNumber) {
            document.querySelector(`#seats .seat[data-seat-number="${selectedSeatNumber}"]`).classList.remove("selected");
        }
        document.querySelector(`#seats .seat[data-seat-number="${seatNumber}"]`).classList.add("selected");
        selectedSeatNumber = seatNumber;
    }

    function confirmReservation() {
        if (selectedSeatNumber) {
            fetch('/yoyaku', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `seat_number=${selectedSeatNumber}`
            })
            .then(response => response.text())
            .then(data => {
                alert(data);
            });
        } else {
            alert("席を選択してください。");
        }
    }
</script>

</body>
</html>