from flask import Flask, render_template_string, jsonify
from datetime import datetime, timezone
import os

# ============================================================
# CONFIGURATION
# ============================================================

GITHUB_REPO_URL = "https://github.com/your-username/your-repo-name"

application = Flask(__name__)


# ============================================================
# PROFESSIONAL CLOUD DASHBOARD
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>AURA Cloud Platform</title>

    <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                Helvetica,
                Arial,
                sans-serif;

            min-height: 100vh;

            color: #172033;

            background:
                linear-gradient(
                    135deg,
                    #f8fbff 0%,
                    #eef5ff 45%,
                    #f8f3ff 100%
                );
        }


        /* =====================================================
           TOP RAINBOW ACCENT
           ===================================================== */

        .rainbow-line {

            position: fixed;

            top: 0;
            left: 0;

            width: 100%;
            height: 4px;

            background:
                linear-gradient(
                    90deg,
                    #ff4b4b,
                    #ff9f43,
                    #feca57,
                    #1dd1a1,
                    #48dbfb,
                    #5f27cd,
                    #ff6b81
                );

            z-index: 100;
        }


        /* =====================================================
           PAGE CONTAINER
           ===================================================== */

        .container {

            width: min(1180px, 92%);

            margin: auto;
        }


        /* =====================================================
           NAVBAR
           ===================================================== */

        header {

            padding: 28px 0;

            border-bottom:
                1px solid rgba(30, 50, 80, 0.08);
        }


        .navbar {

            display: flex;

            align-items: center;

            justify-content: space-between;
        }


        .brand {

            display: flex;

            align-items: center;

            gap: 13px;
        }


        .brand-icon {

            width: 40px;
            height: 40px;

            border-radius: 12px;

            display: flex;

            align-items: center;
            justify-content: center;

            font-size: 20px;

            color: white;

            background:
                linear-gradient(
                    135deg,
                    #5b5ce2,
                    #8b5cf6
                );

            box-shadow:
                0 8px 20px rgba(91,92,226,0.25);
        }


        .brand-name {

            font-size: 18px;

            font-weight: 700;

            letter-spacing: -0.3px;
        }


        .brand-subtitle {

            font-size: 11px;

            color: #7a8499;

            margin-top: 2px;

            letter-spacing: 0.5px;
        }


        .region {

            display: flex;

            align-items: center;

            gap: 8px;

            padding: 9px 15px;

            border-radius: 30px;

            background: white;

            border:
                1px solid rgba(30,50,80,0.08);

            box-shadow:
                0 5px 20px rgba(40,60,100,0.05);

            font-size: 12px;

            color: #536078;
        }


        .status-dot {

            width: 8px;
            height: 8px;

            border-radius: 50%;

            background: #16c784;

            box-shadow:
                0 0 0 4px rgba(22,199,132,0.12);
        }


        /* =====================================================
           HERO
           ===================================================== */

        .hero {

            padding: 65px 0 45px;

            text-align: center;
        }


        .eyebrow {

            display: inline-flex;

            align-items: center;

            gap: 8px;

            padding: 7px 14px;

            border-radius: 30px;

            background: rgba(91,92,226,0.08);

            color: #5557c8;

            font-size: 12px;

            font-weight: 700;

            letter-spacing: 1px;

            text-transform: uppercase;

            margin-bottom: 22px;
        }


        .hero h1 {

            font-size:
                clamp(42px, 6vw, 72px);

            line-height: 1.05;

            letter-spacing: -3px;

            font-weight: 800;

            color: #141a2a;

            margin-bottom: 20px;
        }


        .gradient-text {

            background:
                linear-gradient(
                    90deg,
                    #5557d9,
                    #8b5cf6,
                    #d946ef
                );

            -webkit-background-clip: text;

            -webkit-text-fill-color: transparent;
        }


        .hero-description {

            max-width: 650px;

            margin: auto;

            font-size: 17px;

            line-height: 1.7;

            color: #667085;
        }


        /* =====================================================
           DASHBOARD
           ===================================================== */

        .dashboard {

            display: grid;

            grid-template-columns:
                1.5fr
                1fr;

            gap: 22px;

            margin-bottom: 40px;
        }


        .card {

            background:
                rgba(255,255,255,0.86);

            border:
                1px solid rgba(30,50,80,0.07);

            border-radius: 22px;

            padding: 30px;

            box-shadow:
                0 15px 45px rgba(40,60,100,0.08);

            backdrop-filter: blur(10px);
        }


        .card-header {

            display: flex;

            justify-content: space-between;

            align-items: center;

            margin-bottom: 28px;
        }


        .card-title {

            font-size: 14px;

            font-weight: 700;

            color: #30394d;

            text-transform: uppercase;

            letter-spacing: 0.8px;
        }


        .badge {

            padding: 6px 11px;

            border-radius: 20px;

            font-size: 11px;

            font-weight: 700;
        }


        .badge-success {

            color: #087443;

            background:
                rgba(22,199,132,0.10);
        }


        /* =====================================================
           DEPLOYMENT STATUS
           ===================================================== */

        .deployment {

            display: flex;

            align-items: center;

            gap: 20px;

            margin-bottom: 28px;
        }


        .success-icon {

            width: 58px;
            height: 58px;

            flex-shrink: 0;

            border-radius: 18px;

            display: flex;

            align-items: center;
            justify-content: center;

            font-size: 27px;

            color: #079455;

            background:
                rgba(22,199,132,0.10);
        }


        .deployment h2 {

            font-size: 28px;

            letter-spacing: -0.8px;

            color: #151b2c;
        }


        .deployment p {

            margin-top: 5px;

            font-size: 14px;

            color: #7a8499;
        }


        /* =====================================================
           ENVIRONMENT
           ===================================================== */

        .environment {

            padding: 18px;

            border-radius: 14px;

            background: #f7f8fc;

            border:
                1px solid #edf0f6;

            margin-bottom: 22px;
        }


        .environment-label {

            font-size: 10px;

            text-transform: uppercase;

            color: #8b95a7;

            letter-spacing: 1px;

            margin-bottom: 7px;
        }


        .environment-value {

            font-size: 15px;

            font-weight: 600;

            color: #30394d;
        }


        /* =====================================================
           PIPELINE
           ===================================================== */

        .pipeline {

            display: flex;

            align-items: center;

            justify-content: space-between;

            padding-top: 10px;
        }


        .pipeline-step {

            text-align: center;

            flex: 1;

            position: relative;
        }


        .pipeline-step:not(:last-child)::after {

            content: "";

            position: absolute;

            top: 14px;

            left: 65%;

            width: 70%;

            height: 2px;

            background: #dfe4ec;
        }


        .pipeline-dot {

            position: relative;

            z-index: 2;

            margin: auto;

            width: 28px;
            height: 28px;

            border-radius: 50%;

            display: flex;

            align-items: center;
            justify-content: center;

            background: #16c784;

            color: white;

            font-size: 12px;
        }


        .pipeline-label {

            font-size: 10px;

            color: #7a8499;

            margin-top: 8px;
        }


        /* =====================================================
           SYSTEM STATS
           ===================================================== */

        .stats {

            display: grid;

            grid-template-columns:
                1fr 1fr;

            gap: 12px;
        }


        .stat {

            padding: 18px;

            border-radius: 15px;

            background: #f8f9fc;

            border:
                1px solid #edf0f5;
        }


        .stat-label {

            font-size: 10px;

            text-transform: uppercase;

            color: #8993a5;

            letter-spacing: 0.8px;

            margin-bottom: 8px;
        }


        .stat-value {

            font-size: 15px;

            font-weight: 700;

            color: #30394d;
        }


        .stat-value.green {

            color: #079455;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .actions {

            margin-top: 22px;
        }


        .button {

            display: block;

            width: 100%;

            padding: 13px 18px;

            margin-top: 10px;

            text-align: center;

            text-decoration: none;

            border-radius: 12px;

            font-size: 13px;

            font-weight: 700;

            transition: all 0.2s ease;
        }


        .button-primary {

            color: white;

            background:
                linear-gradient(
                    135deg,
                    #5557d9,
                    #7c3aed
                );

            box-shadow:
                0 8px 20px rgba(91,92,226,0.20);
        }


        .button-secondary {

            color: #505a70;

            background: white;

            border:
                1px solid #e2e6ed;
        }


        .button:hover {

            transform: translateY(-2px);

            box-shadow:
                0 10px 25px rgba(40,60,100,0.12);
        }


        /* =====================================================
           FOOTER
           ===================================================== */

        footer {

            padding: 30px 0 35px;

            border-top:
                1px solid rgba(30,50,80,0.08);

            color: #8993a5;

            font-size: 12px;

            text-align: center;
        }


        .footer-brand {

            font-weight: 700;

            color: #5c6475;
        }


        /* =====================================================
           RESPONSIVE
           ===================================================== */

        @media (max-width: 850px) {

            .dashboard {

                grid-template-columns: 1fr;
            }

            .hero {

                padding-top: 45px;
            }

            .hero h1 {

                letter-spacing: -2px;
            }

        }


        @media (max-width: 550px) {

            .navbar {

                flex-direction: column;

                gap: 15px;
            }

            .stats {

                grid-template-columns: 1fr;
            }

            .pipeline-label {

                font-size: 9px;
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

    <div class="rainbow-line"></div>


    <!-- ======================================================
         HEADER
         ====================================================== -->

    <header>

        <div class="container">

            <div class="navbar">

                <div class="brand">

                    <div class="brand-icon">
                        ☁
                    </div>

                    <div>

                        <div class="brand-name">
                            AURA Cloud Platform
                        </div>

                        <div class="brand-subtitle">
                            APPLICATION OPERATIONS
                        </div>

                    </div>

                </div>


                <div class="region">

                    <span class="status-dot"></span>

                    AWS REGION:
                    {{ aws_region }}

                </div>

            </div>

        </div>

    </header>


    <!-- ======================================================
         HERO
         ====================================================== -->

    <section class="hero">

        <div class="container">

            <div class="eyebrow">
                ● Production Environment
            </div>


            <h1>

                Deployment
                <span class="gradient-text">
                    Successful
                </span>

            </h1>


            <p class="hero-description">

                Your application has been successfully deployed
                and is currently running on AWS Elastic Beanstalk.

                All core application services are operational.

            </p>

        </div>

    </section>


    <!-- ======================================================
         DASHBOARD
         ====================================================== -->

    <main class="container">

        <div class="dashboard">


            <!-- LEFT CARD -->

            <div class="card">

                <div class="card-header">

                    <div class="card-title">
                        Deployment Overview
                    </div>

                    <div class="badge badge-success">
                        OPERATIONAL
                    </div>

                </div>


                <div class="deployment">

                    <div class="success-icon">
                        ✓
                    </div>

                    <div>

                        <h2>
                            Application Online
                        </h2>

                        <p>
                            Flask / Gunicorn runtime initialized successfully
                        </p>

                    </div>

                </div>


                <div class="environment">

                    <div class="environment-label">
                        Environment
                    </div>

                    <div class="environment-value">
                        {{ env_name }}
                    </div>

                </div>


                <!-- PIPELINE -->

                <div class="pipeline">

                    <div class="pipeline-step">

                        <div class="pipeline-dot">
                            ✓
                        </div>

                        <div class="pipeline-label">
                            SOURCE
                        </div>

                    </div>


                    <div class="pipeline-step">

                        <div class="pipeline-dot">
                            ✓
                        </div>

                        <div class="pipeline-label">
                            BUILD
                        </div>

                    </div>


                    <div class="pipeline-step">

                        <div class="pipeline-dot">
                            ✓
                        </div>

                        <div class="pipeline-label">
                            DEPLOY
                        </div>

                    </div>


                    <div class="pipeline-step">

                        <div class="pipeline-dot">
                            ✓
                        </div>

                        <div class="pipeline-label">
                            HEALTH
                        </div>

                    </div>

                </div>

            </div>


            <!-- RIGHT CARD -->

            <div class="card">

                <div class="card-header">

                    <div class="card-title">
                        System Status
                    </div>

                    <div class="badge badge-success">
                        HEALTHY
                    </div>

                </div>


                <div class="stats">


                    <div class="stat">

                        <div class="stat-label">
                            Environment
                        </div>

                        <div class="stat-value">
                            AWS EB
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-label">
                            Runtime
                        </div>

                        <div class="stat-value">
                            Python
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-label">
                            Framework
                        </div>

                        <div class="stat-value">
                            Flask
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-label">
                            Application
                        </div>

                        <div class="stat-value green">
                            ● ONLINE
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-label">
                            Server Time
                        </div>

                        <div
                            id="server-time"
                            class="stat-value">

                            {{ current_time }}

                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-label">
                            Region
                        </div>

                        <div class="stat-value">
                            {{ aws_region }}
                        </div>

                    </div>

                </div>


                <div class="actions">

                    <a
                        href="/health"
                        class="button button-primary">

                        Run Health Check

                    </a>


                    <a
                        href="{{ github_url }}"
                        target="_blank"
                        class="button button-secondary">

                        View Source Repository

                    </a>

                </div>

            </div>

        </div>

    </main>


    <!-- ======================================================
         FOOTER
         ====================================================== -->

    <footer>

        <div class="container">

            <span class="footer-brand">
                AURA Cloud Platform
            </span>

            &nbsp; · &nbsp;

            AWS Elastic Beanstalk

            &nbsp; · &nbsp;

            Flask

            &nbsp; · &nbsp;

            Gunicorn

        </div>

    </footer>


</body>

</html>
"""


# ============================================================
# HOME
# ============================================================

@application.route('/')
def home():

    now = datetime.now(timezone.utc).strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    env_name = os.environ.get(
        'AWS_EB_ENVIRONMENT_NAME',
        'LOCAL_DEBUG'
    )

    aws_region = os.environ.get(
        'AWS_REGION',
        'eu-north-1'
    )

    return render_template_string(

        HTML_TEMPLATE,

        current_time=now,

        github_url=GITHUB_REPO_URL,

        env_name=env_name,

        aws_region=aws_region

    )


# ============================================================
# HEALTH CHECK
# ============================================================

@application.route('/health')
def health_check():

    return jsonify({

        "status": "nominal",

        "service_id": "aura-core-1",

        "timestamp_utc":
            datetime.now(timezone.utc).isoformat()

    }), 200


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == '__main__':

    application.run(

        host='0.0.0.0',

        port=5000

    )
