#!/usr/bin/env python3
"""Run repository and portable-package smoke checks on a trusted checkout."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = (
    ('cluster_keywords.py', 'examples/keyword-clustering/input.json'),
    ('audit_topic_graph.py', 'examples/topical-architecture/sample.json'),
    ('prioritize_opportunities.py', 'examples/opportunity-prioritization/sample.json'),
    ('audit_locale_manifest.py', 'examples/locale-audit/sample.json'),
    ('validate_research.py', 'examples/research-handoff/sample.json'),
    ('inspect_architecture.py', 'examples/architecture/sample.json'),
    ('audit_rendering.py', 'examples/rendering/sample.json'),
    ('audit_next_delivery.py', 'examples/next-delivery/sample.json'),
)


def main():
    results = []
    def run(name, cwd, args, expected=0):
        try:
            code = subprocess.run([sys.executable, *args], cwd=cwd, timeout=120).returncode
            results.append({'check':name, 'expected':expected, 'actual':code, 'pass':code == expected})
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append({'check':name,'pass':False,'error':str(exc)})
        return results[-1]['pass']

    def smoke(root, label, out):
        run(label + ': docs', root, ['scripts/check_docs.py'])
        run(label + ': HTML valid', root, ['scripts/audit_html.py','--manifest','examples/routes.json','--root','examples/site'])
        run(label + ': HTML intentional failure', root, ['scripts/audit_html.py','--manifest','examples/routes-failing.json','--root','examples/site'], 1)
        run(label + ': audit_spa_build.py', root, ['scripts/audit_spa_build.py','--input','examples/spa-build/sample.json','--root','examples/spa-build/artifacts','--output',str(out / (label + '-audit_spa_build.py.json'))])
        for script, fixture in FIXTURES:
            run(label + ': ' + script, root, ['scripts/' + script,'--input',fixture,'--output',str(out / (label + '-' + script + '.json'))])

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        run('repository unit tests', ROOT, ['-m','unittest','discover','-s','tests','-v'])
        smoke(ROOT, 'repo', work)
        archive = work / 'skill.zip'
        if run('build portable skill', ROOT, ['scripts/build_skill.py','--out',str(archive)]):
            try:
                with ZipFile(archive) as z:
                    names = z.namelist()
                    if z.testzip() or len(names) != len(set(names)) or any(
                        Path(n).is_absolute() or '..' in Path(n).parts or
                        not n.startswith('seo-engineering/') or
                        set(Path(n).parts) & {'private','projects','.git'}
                        for n in names
                    ):
                        raise ValueError('archive integrity or scope check failed')
                    z.extractall(work)
                skill = work / 'seo-engineering'
                library = skill / 'references/library'
                required = [skill / 'SKILL.md', skill / 'references/router.md', skill / 'references/execution-contract.md']
                if not all(p.is_file() for p in required):
                    raise ValueError('missing entrypoint or routing files')
                results.append({'check':'archive structure','pass':True})
                smoke(library, 'package', work)
                for script in [name for name, _ in FIXTURES] + ['audit_spa_build.py']:
                    left, right = [work / (label + '-' + script + '.json') for label in ('repo','package')]
                    equal = left.is_file() and right.is_file() and left.read_bytes() == right.read_bytes()
                    results.append({'check':'fixture parity: '+script,'pass':equal})
            except (OSError, ValueError) as exc:
                results.append({'check':'archive checks','pass':False,'error':str(exc)})
    print(json.dumps({'checks':results, 'behavioral_evaluations':'not_run',
                      'external_installation':'not_run', 'human_review':'required'},indent=2))
    return 0 if all(x['pass'] for x in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
