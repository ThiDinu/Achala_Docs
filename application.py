from flask import Flask, render_template_string, jsonify
from datetime import datetime
import os

# Specify your actual GitHub repository URL here
GITHUB_REPO_URL = "https://github.com/your-username/your-repo-name"

application = Flask(__name__)

# Rainbow-themed HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Rainbow Cloud | AWS Elastic Beanstalk</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            min-height: 100vh;
            font-family: Arial, Helvetica, sans-serif;

            background:
                linear-gradient(
                    135deg,
                    #ff0000,
                    #ff7f00,
                    #ffff00,
                    #00ff00,
                    #00bfff,
                    #0000ff,
                    #8b00ff
                );

            background-size: 400% 400%;
            animation: rainbowBackground 12s ease infinite;

            color: #ffffff;
            display: flex;
            flex-direction: column;
        }

        @keyframes rainbowBackground {
            0% {
                background-position: 0% 50%;
            }

            50% {
                background-position: 100% 50%;
            }

            100% {
                background-position: 0% 50%;
            }
        }

        .overlay {
            min-height: 100vh;
            background: rgba(0, 0, 0, 0.20);
            padding: 25px;
        }

        header {
            max-width: 1200px;
            margin: auto;
            padding: 20px 25px;

            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(12px);

            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 18px;

            display: flex;
            justify-content: space-between;
            align-items: center;

            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        .rainbow-dot {
            width: 18px;
            height: 18px;
            border-radius: 50%;

            background: linear-gradient(
                135deg,
                red,
                orange,
                yellow,
                green,
                blue,
                purple
            );

            box-shadow: 0 0 15px rgba(255,255,255,0.8);
        }

        .region {
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 13px;
        }

        main {
            max-width: 1200px;
            width: 100%;
            margin: auto;
            padding: 40px 0;

            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 25px;
        }

        .card {
            background: rgba(255,255,255,0.18);
            backdrop-filter: blur(15px);

            border: 1px solid rgba(255,255,255,0.4);
            border-radius: 25px;

            padding: 35px;

            box-shadow:
                0 15px 40px rgba(0,0,0,0.18);

            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .main-card {
            min-height: 500px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        h1 {
            font-size: clamp(40px, 6vw, 75px);
            font-weight: 900;
            line-height: 1;
            margin-bottom: 20px;

            text-shadow: 3px 3px 10px rgba(0,0,0,0.2);
        }

        .success {
            display: inline-block;

            background: rgba(0, 200, 80, 0.85);
            padding: 10px 20px;

            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;

            margin-bottom: 25px;
        }

        .message {
            font-size: 20px;
            line-height: 1.7;
        }

        .environment {
            margin-top: 20px;

            background: rgba(0,0,0,0.18);
            padding: 15px;

            border-radius: 12px;

            font-family: monospace;
        }

        .terminal {
            background: rgba(0,0,0,0.45);

            padding: 20px;
            border-radius: 15px;

            font-family: monospace;
            font-size: 14px;

            line-height: 1.8;
        }

        .terminal .ok {
            color: #7cff9b;
            font-weight: bold;
        }

        .stats-title {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 25px;
        }

        .stat {
            background: rgba(255,255,255,0.16);

            padding: 18px;
            border-radius: 15px;

            margin-bottom: 15px;
        }

        .stat-label {
            font-size: 12px;
            opacity: 0.75;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            font-size: 20px;
            font-weight: bold;
            margin-top: 6px;
        }

        .health {
            color: #7cff9b;
        }

        .button {
            display: block;

            text-align: center;
            text-decoration: none;

            padding: 15px;
            margin-top: 15px;

            border-radius: 30px;

            background: rgba(255,255,255,0.25);
            color: white;

            border: 1px solid rgba(255,255,255,0.5);

            font-weight: bold;

            transition: all 0.3s ease;
        }

        .button:hover {
            background: white;
            color: #7b2cff;
            transform: scale(1.03);
        }

        footer {
            max-width: 1200px;
            width: 100%;
            margin: auto;

            text-align: center;
            padding: 20px;

            font-size: 13px;
            opacity: 0.85;
        }

        @media (max-width: 800px) {
            main {
                grid-template-columns: 1fr;
            }

            header {
                flex-direction: column;
                gap: 15px;
                text-align: center;
            }

            .main-card {
                min-height: auto;
            }
        }
    </style>

    <script>
        function updateClock() {
            const now = new Date();

            document.getElementById("server-time").textContent =
                now.toISOString()
                   .replace("T", " ")
                   .substring(0, 19) + " UTC";
        }

        setInterval(updateClock, 1000);

        window.onload = updateClock;
    </script>

</head>

<body>

<div class="overlay">

    <!-- HEADER -->
    <header>

        <div class="logo">
            <div class="rainbow-dot"></div>
            <span>AURA CLOUD</span>
        </div>

        <div class="region">
            AWS REGION: {{ aws_region }}
        </div>

    </header>


    <!-- MAIN -->
    <main>

        <!-- LEFT CARD -->
        <div class="card main-card">

            <div>

                <div class="success">
                    ✓ DEPLOYMENT SUCCESS
                </div>

                <h1>
                    RAINBOW<br>
                    CLOUD
                </h1>

                <div class="message">

                    <p>
                        🌈 Your Flask application is running successfully!
                    </p>

                    <p style="margin-top: 15px;">
                        AWS Elastic Beanstalk has successfully
                        initialized the Python/Gunicorn runtime.
                    </p>

                </div>

                <div class="environment">
                    ENVIRONMENT: {{ env_name }}
                </div>

            </div>


            <!-- TERMINAL -->

            <div class="terminal">

                <div>> INITIALIZING EB DEPLOYMENT... <span class="ok">[OK]</span></div>

                <div>> VERIFYING REQUIREMENTS.TXT... <span class="ok">[OK]</span></div>

                <div>> STARTING GUNICORN... <span class="ok">[OK]</span></div>

                <div>> APPLICATION HEALTH CHECK... <span class="ok">[OK]</span></div>

                <div class="ok">
                    > > > SYSTEM READY 🌈
                </div>

            </div>

        </div>


        <!-- RIGHT CARD -->

        <div class="card">

            <div class="stats-title">
                ☁ SYSTEM STATUS
            </div>


            <div class="stat">

                <div class="stat-label">
                    Server Time UTC
                </div>

                <div
                    id="server-time"
                    class="stat-value">
                    {{ current_time }}
                </div>

            </div>


            <div class="stat">

                <div class="stat-label">
                    Environment Health
                </div>

                <div class="stat-value health">
                    ● NOMINAL
                </div>

            </div>


            <div class="stat">

                <div class="stat-label">
                    Platform
                </div>

                <div class="stat-value">
                    Flask + Gunicorn
                </div>

            </div>


            <div class="stat">

                <div class="stat-label">
                    Cloud Platform
                </div>

                <div class="stat-value">
                    AWS Elastic Beanstalk
                </div>

            </div>


            <a href="/health" class="button">
                🔍 RUN HEALTH CHECK
            </a>


            <a
                href="{{ github_url }}"
                target="_blank"
                class="button">

                💻 SOURCE CODE

            </a>

        </div>

    </main>


    <!-- FOOTER -->

    <footer>

        🌈 AURA CLOUD SYSTEM
        &nbsp; • &nbsp;
        AWS Elastic Beanstalk
        &nbsp; • &nbsp;
        Flask

    </footer>

</div>

</body>
</html>
"""


@application.route('/')
def home():

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Get environment name from AWS metadata if available
    env_name = os.environ.get(
        'AWS_EB_ENVIRONMENT_NAME',
        'LOCAL_DEBUG'
    )

    aws_region = os.environ.get(
        'AWS_REGION',
        'us-east-1'
    )

    return render_template_string(
        HTML_TEMPLATE,

        current_time=now,

        github_url=GITHUB_REPO_URL,

        env_name=env_name,

        aws_region=aws_region
    )


@application.route('/health')
def health_check():

    return jsonify({

        "status": "nominal",

        "service_id": "aura-core-1",

        "timestamp_utc":
            datetime.utcnow().isoformat()

    }), 200


if __name__ == '__main__':

    # Local development server execution

    application.run(
        host='0.0.0.0',
        port=5000
    )
