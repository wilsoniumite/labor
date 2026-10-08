# Writes results/explore_youth_school.json from the spec log and the candidate definitions.
import json, os
L = [json.loads(l) for l in open('explore/youth_school/specs_log.jsonl')]
by = {r['label'].split()[0]: r for r in L}
out = dict(
    theme='youth_school', half='explore', geos_n=16, specifications_estimated=46,
    loo_reruns=47, specs=L,
    candidates=[
        dict(id='E1', varies_P='C6 (regressor lagged one year)', outcome='educ2024 (edat_lfse_19 POP FE Y20-24 T)',
             regressor='U2554_{t-1} (C7 rule: une_rt_a else lfsa_urgan, per country)', controls_fe='geo + year FE, C3 breaks; no controls',
             years='1997-2025 excl. 2020-2021 (effective 2004-2025)', side=1, explore=by['S10'], variants_tried=9,
             loo=json.load(open('explore/youth_school/loo_school.json'))['S10'], trends=by['S12']),
        dict(id='E2', varies_P='D1 (outcome E 20-24 instead of A 25-34)', outcome='E2024 (lfsa_ergan NAT, mean of M and F)',
             regressor='log q_{t-1} x F_c', controls_fe='geo + year FE, log q_{t-1}, U, C3 breaks',
             years='1997-2025 excl. 2020-2021', side=-1, explore=by['N3'], variants_tried=7, trends=by['K1']),
    ],
    common_shift=json.load(open('explore/youth_school/common_shift.json')),
)
json.dump(out, open('results/explore_youth_school.json', 'w'), indent=1)
print('ok', len(L))
