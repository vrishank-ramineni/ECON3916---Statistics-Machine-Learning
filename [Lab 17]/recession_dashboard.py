import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression


@st.cache_data
def load_fred_data():
    """Load FRED recession and yield spread data, or fall back to sample data."""
    try:
        import fredapi
        fred = fredapi.Fred(api_key='09c92627a64eac09d828963a22009114')  # <-- Replace this with your own key
        spread_raw = fred.get_series('T10Y3M', observation_start='1970-01-01')
        recession_raw = fred.get_series('USREC', observation_start='1970-01-01')

        spread_monthly = spread_raw.resample('ME').last()
        recession_monthly = recession_raw.resample('ME').max()

        df = pd.DataFrame({
            'yield_spread': spread_monthly,
            'recession': recession_monthly
        }).dropna()
        return df

    except Exception as e:
        st.warning(f"FRED load failed ({e}); using fallback sample data.")
        date_index = pd.date_range('2020-01-01', periods=80, freq='ME')
        return pd.DataFrame({
            'yield_spread': np.tile([0.5, 0.3, -0.1, 0.2, 0.1, -0.2, 0.4, -0.3, 0.6, 0.0], 8),
            'recession': np.tile([0, 0, 1, 0, 0, 1, 0, 0, 0, 1], 8)
        }, index=date_index)


@st.cache_data
def bootstrap_confidence_band(X, y, n_bootstrap):
    """Build a bootstrapped 90% confidence band for recession probability."""
    n = len(X)
    boot_preds = np.zeros((n_bootstrap, n))

    for b in range(n_bootstrap):
        # Resample indices with replacement to create an alternate dataset.
        boot_idx = np.random.choice(n, size=n, replace=True)
        X_boot = X[boot_idx]
        y_boot = y[boot_idx]

        # Refit a fresh logistic model on the bootstrap sample.
        boot_model = LogisticRegression(random_state=b, max_iter=1000)
        boot_model.fit(X_boot, y_boot)

        # Predict probabilities back on the original data points.
        boot_preds[b, :] = boot_model.predict_proba(X)[:, 1]

    # The 5th and 95th percentiles across bootstrap replications
    # form the 90% confidence band.
    lower = np.percentile(boot_preds, 5, axis=0)
    upper = np.percentile(boot_preds, 95, axis=0)
    return lower, upper


def build_model(df, lag_months):
    df = df.copy()
    df[f'yield_spread_lag{lag_months}'] = df['yield_spread'].shift(lag_months)
    df = df.dropna()

    X = df[[f'yield_spread_lag{lag_months}']].values
    y = df['recession'].values

    if X.shape[0] == 0:
        raise ValueError(
            f'Not enough observations after applying a {lag_months}-month lag. '
            'Please choose a shorter horizon or provide a longer dataset.'
        )

    logit_model = LogisticRegression(random_state=42, max_iter=1000)
    logit_model.fit(X, y)

    df['recession_prob'] = logit_model.predict_proba(X)[:, 1]
    return df, logit_model, X, y


def get_recession_bands(df_in):
    bands = []
    in_rec = False
    start = None
    for date, val in df_in['recession'].items():
        if val == 1 and not in_rec:
            start = date
            in_rec = True
        elif val == 0 and in_rec:
            bands.append((start, date))
            in_rec = False
    if in_rec:
        bands.append((start, df_in.index[-1]))
    return bands


def plot_probability_series(df_plot, lag_months):
    recession_bands = get_recession_bands(df_plot)

    fig = go.Figure()
    for i, (start, end) in enumerate(recession_bands):
        fig.add_vrect(
            x0=start,
            x1=end,
            fillcolor='rgba(214,39,40,0.12)',
            line_width=0,
            annotation_text='NBER Recession' if i == 0 else None,
            annotation_position='top left'
        )

    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot['ci_upper'] * 100,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot['ci_lower'] * 100,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(31,119,180,0.15)',
        name='90% Bootstrap CI'
    ))

    fig.add_trace(go.Scatter(
        x=df_plot.index,
        y=df_plot['recession_prob'] * 100,
        mode='lines',
        line=dict(color='#1f77b4', width=2.5),
        name=f'P(Recession in {lag_months}m)',
        hovertemplate='%{x|%b %Y}<br>P(Recession) = %{y:.1f}%<extra></extra>'
    ))

    fig.add_hline(y=50, line_dash='dash', line_color='black', opacity=0.4,
                  annotation_text='50% threshold', annotation_position='bottom right')

    fig.update_layout(
        title=f'Recession Probability — {lag_months}-Month Forecast Horizon',
        yaxis=dict(title='Recession Probability (%)', range=[0, 105]),
        xaxis=dict(title='Date'),
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=60, r=20, t=80, b=40),
        height=520
    )
    return fig


def main():
    st.set_page_config(page_title='NY Fed Recession Dashboard', layout='wide')

    st.title('📉 NY Fed Yield Curve Recession Model')
    st.markdown(
        'Interactive dashboard for logistic regression recession probability forecasting ' 
        'using the 10Y-3M spread and FRED data.'
    )

    df_raw = load_fred_data()

    st.sidebar.header('Model Controls')
    lag_months = st.sidebar.select_slider(
        'Prediction Horizon (months ahead)',
        options=[6, 12, 18],
        value=12
    )
    n_bootstrap = st.sidebar.slider('Bootstrap iterations', 50, 500, 200, step=50)
    start_year = st.sidebar.slider('Start year', 1975, 2020, 2000)

    df, logit_model, X, y = build_model(df_raw, lag_months)
    ci_lower, ci_upper = bootstrap_confidence_band(X, y, n_bootstrap)
    df['ci_lower'] = ci_lower
    df['ci_upper'] = ci_upper

    current_row = df.iloc[-1]
    current_spread = current_row[f'yield_spread_lag{lag_months}']
    current_prob = current_row['recession_prob']
    current_date = current_row.name

    st.sidebar.header('Current Model Output')
    st.sidebar.metric('Date', current_date.strftime('%Y-%m'))
    st.sidebar.metric('Lagged Spread', f'{current_spread:.2f} pp')
    st.sidebar.metric('P(Recession)', f'{current_prob:.1%}')
    st.sidebar.markdown(
        f"**Logit intercept:** {logit_model.intercept_[0]:.4f}  \n"
        f"**Logit slope:** {logit_model.coef_[0][0]:.4f}  \n"
        f"**Odds ratio:** {np.exp(logit_model.coef_[0][0]):.4f}  \n"
        f"**Sample size:** {len(df):,}  \n"
        f"**Bootstrap reps:** {n_bootstrap}"
    )

    st.markdown('---')

    df_plot = df[f'{start_year}':].copy()
    fig = plot_probability_series(df_plot, lag_months)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander('How to interpret the 90% confidence band'):
        st.markdown(
            'The shaded band is built by repeatedly resampling the training data with replacement, ' 
            'fitting a new logistic model on each resampled dataset, and then predicting recession ' 
            'probability on the original dates. This produces many alternative probability ' 
            'trajectories, and the 5th/95th percentiles of those trajectories form the band. '
            '\n\n'
            '**Narrow band** means the model prediction is stable: slightly different samples ' 
            'produce similar probabilities. **Wide band** means more uncertainty: the predicted ' 
            'probability depends more on which observations are included in the sample. '
            '\n\n'
            'During the 2022–2024 inversion, the band should generally be narrower than average if ' 
            'the yield spread is far into the extreme inversion region, because the sigmoid curve ' 
            'flattens and many bootstrap models agree on a high probability. If the band is wide ' 
            'there, it indicates that the exact probability is still uncertain despite the inversion.'
        )

    st.markdown('---')
    st.markdown('### Model summary')
    st.write(df[['yield_spread', f'yield_spread_lag{lag_months}', 'recession', 'recession_prob']].tail(12))


if __name__ == '__main__':
    main()
