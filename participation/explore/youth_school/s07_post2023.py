# Entrants since 2023: C-4's window (2016-2019, 2022-2025), F_c x 1[year >= 2023] as the moderator.
from youth import *
v, cl = man()
keys = ['gapU', 'gapUL', 'U1529', 'U2554', 'educ2024', 'gapE', 'E2024', 'E2554', 'U', 'notEnotS2024', 'nonemp_inac2529']
df, br = frame({k: v[k] for k in keys}, years=[2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025])
df['F'] = df.geo.map(cl['F_c']); df['X'] = df.geo.map(cl['X_c'])
df['post'] = (df.year >= 2023).astype(float)
df['Fpost'] = df.F * df.post; br.alias('Fpost')
d = df.dropna(subset=['F'])
reg('P1 gapU ~ F x post | U', d, br, 'gapU', 'Fpost', ['U'], side=-1)
reg('P2 educ2024 ~ F x post | U', d, br, 'educ2024', 'Fpost', ['U'], side=1)
reg('P3 gapE ~ F x post | U', d, br, 'gapE', 'Fpost', ['U'], side=-1)
reg('P4 E2024 ~ F x post | U', d, br, 'E2024', 'Fpost', ['U'], side=-1)
reg('P5 gapU ~ F x post | U, trends', d, br, 'gapU', 'Fpost', ['U'], side=-1, trends=True)
reg('P6 educ2024 ~ F x post | U, trends', d, br, 'educ2024', 'Fpost', ['U'], side=1, trends=True)
