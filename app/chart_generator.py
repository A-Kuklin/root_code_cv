import pandas as pd
import matplotlib.pyplot as plt
import io
import asyncpg
from settings import settings


async def generate_chart():
    # dsn = settings.docker_db_url if settings.docker_flag else settings.db_url
    conn = await asyncpg.connect(dsn=settings.db_url)
    rows = await conn.fetch('SELECT datetime, plan, fact FROM data')

    df = pd.DataFrame(rows, columns=['datetime', 'plan', 'fact'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['time'] = df['datetime'].dt.strftime(settings.time_format)
    df.drop(columns=['datetime'], inplace=True)
    df_grouped = df.groupby('time').sum()

    plt.figure()
    ax = df_grouped.plot(kind='bar')
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Values')
    ax.set_title('Plan vs Fact')
    ax.legend()
    labels = ax.get_xticklabels()
    for label in labels:
        label.set_rotation(90)
    plt.subplots_adjust(bottom=0.36)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    await conn.close()

    return buf



