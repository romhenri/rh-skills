---
name: seed-test-scenario
description: Create test users, activities and data in the local or staging database for a flow the user wants to test, then hand back the credentials in a table, a short step-by-step test script, and a cleanup offer. Use when the user says "crie usuário/professor de teste", "crie no banco de staging um caso de testes e me dê qual user", "me dê as credenciais", "me dê o roteiro (de teste)", "popule o banco local/do stg", or asks for a test scenario with N users/questions/answers. Writes to databases, so it always confirms the target first and goes through the project's dry-run/target guard.
argument-hint: "[flow to test] [target: local|stg]"
disable-model-invocation: true
model: opus
---

# Seed Test Scenario

Build the smallest dataset that lets the user exercise one flow, in the database they
chose, and hand back everything needed to test it: who to log in as, what to click,
and how to clean up.

**IS:** minimal, targeted test data + credentials + a test script.
**IS NOT:** loading production-like volumes, migrating schema, or touching prd.

## Phase 1: Pin the target and the flow

**Objective:** know exactly which database will be written and what the user will test.

1. **Learn the project's guard rails first.** Read CLAUDE.md and any DB ops doc
   (`docs/**/database*.md`, `Makefile` help, `scripts/` with a `--dry-run` / `--expect-db` /
   `APPLY=` convention). Follow them literally — they override anything here.
2. **Resolve the target database**: read what the config (`.env`, settings) points at *right
   now* and print `DB name @ host`. Config often changes between sessions — never assume.
3. **Confirm with the user** if any of these is true: the target wasn't named, the config
   points elsewhere than they said, or it's not local. The target name they confirm is what
   goes into `--expect-db` (or the project's equivalent).
4. **prd → refuse.** Test data never goes to production; tell the user and stop.
5. **Staging → check connectivity** before anything else (e.g. `pg_isready -h <host>` or a
   `SELECT 1` with a short timeout). If it fails or times out, say: **"Parece que a VPN está
   desligada — conecte e me avise"**, and stop.
6. **Clarify the flow** only if it's ambiguous: which role logs in (aluno, professor,
   corretor, admin), what they should see, and any volume the user specified
   ("6 questões, 100+ respostas", "3 professores com external ids").

## Phase 2: Plan the minimum data

**Objective:** a short plan the user can sanity-check before any write.

Inspect the models/schema for the entities involved (users, roles, activities, questions,
answers, assignments) and list only what the flow needs:

```
Target: <db> @ <host>
Creates:
- 1 professor   username=teste.prof.<tag>  external_id=<tag>-prof-1
- 1 atividade   "Teste <tag>" with 6 questões, owned by the professor
- 120 respostas spread over 20 alunos
Tag: <tag>  (e.g. qa-20261126-stressed — prefixed on every name/external_id for cleanup)
```

- Prefix every created name / external_id / title with a unique **tag** so the data is
  findable and removable later.
- Reuse existing entities when the flow allows (e.g. an existing school) instead of creating parents.
- Passwords: generate a simple, readable one per run (e.g. `Teste@<4 digits>`), hashed with the
  app's own hashing function — never write a plaintext password column.

## Phase 3: Create — dry run, then write

**Objective:** data in the confirmed database, created through the project's guard.

1. **Prefer the project's own tooling**: an existing seed script, make target, admin API,
   or fixture loader. Use it with its dry-run form first.
2. **Otherwise write a one-off script in the scratchpad** (not in the repo) that:
   - uses the app's models, session and password-hashing function (no hand-rolled SQL for passwords);
   - calls the project's target check (e.g. a `check_target(expect_db)` helper) or, if none exists,
     prints `DB @ host` and exits unless it equals the confirmed target;
   - runs in a transaction; `--dry-run` rolls back, the real run commits;
   - prints every created id.
3. Run the dry run, show its output, then run for real with the target guard
   (`--expect-db <db>` / `APPLY=1 EXPECT_DB=<db>` / the project's equivalent).
4. If the project takes a dump before writes to non-local DBs, let it (don't pass `--no-dump`).

## Phase 4: Hand over credentials and the test script

**Objective:** the user can start testing without reading anything else.

```
Ambiente: stg (<db>) · Tag: qa-20261126-stressed

| Papel     | Usuário             | Senha       | Observação                      |
|-----------|---------------------|-------------|---------------------------------|
| professor | teste.prof.stressed | Teste@4821  | dono da atividade 27            |
| aluno     | teste.aluno.01      | Teste@4821  | 6 respostas na atividade 27     |

Roteiro:
1. Abra <URL do ambiente> e entre como teste.prof.stressed.
2. Vá em Atividades → "Teste qa-20261126-stressed" (id 27).
3. Abra a fila de correção — devem aparecer 120 respostas.
4. Corrija uma; confira que o contador cai para 119.
```

- Keep the script to the **simplest path that proves the flow** (≈3–7 steps); if the user asks
  for "o roteiro mais simples possível", cut to the bare minimum.
- Say what the expected result of each key step is, so a failure is obvious.
- Keep the table handy: if asked "me reenvie as credenciais/o roteiro", resend the same table and script.

## Phase 5: Offer cleanup

**Objective:** test data doesn't linger.

End with one line naming exactly what would be removed, e.g.:
**"Quando terminar, posso limpar: atividade 27, 1 professor e 20 alunos com a tag `qa-20261126-stressed`."**

On "limpe a atividade 27" (or similar): list what will be deleted (children included), run the
deletion as a dry run, then for real with the same target guard. Delete only rows carrying this
run's tag or ids — never by broad filters.

## Examples

**Local, quick:**
User: `/seed-test-scenario 3 professores com external ids, local`
→ config points at local compose DB → plan (3 professors, tag `qa-20261126-prof`) → dry run →
create → table with 3 logins → 3-step script (log in, see empty dashboard, external_id shown) → cleanup offer.

**Staging, stress case:**
User: "crie no banco de staging um caso de testes com 6 questões e mais de 100 respostas e me dê qual user"
→ config points at local, user said stg → ask to confirm the switch → connectivity check fails →
"Parece que a VPN está desligada" → user connects → plan → dry run → write with `--expect-db <stgdb>` →
table + script → cleanup offer.

## Key Principles

- The confirmed target name goes into the guard on every write; a mismatch means stop, not override.
- Minimum data for the flow, all tagged — tags are what make cleanup safe.
- Probe with dry runs, never with real writes "to see what happens".
- Use the app's own models and password hashing so the test users behave like real ones.
- Production is out of scope, always.
