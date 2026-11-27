"""감사 스킬 묶음을 내 스킬 폴더(~/.claude/skills)에 복사한다. 다시 돌리면 같은 이름 폴더를 새 판으로 바꾼다.

  python install.py            설치(또는 업데이트)
  python install.py --list     무엇이 어디로 가는지만 보인다

회사 폴더의 자료는 건드리지 않는다. 설치 뒤에는 Claude 앱을 다시 열고 감사 루트에서 「설치 점검」 을 시킨다.
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = Path.home() / ".claude" / "skills"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    skills = sorted(p for p in (HERE / "skills").iterdir() if (p / "SKILL.md").is_file())
    if "--list" in sys.argv:
        for s in skills:
            print(f"{s.name}  ->  {DEST / s.name}")
        return 0
    DEST.mkdir(parents=True, exist_ok=True)
    for s in skills:
        d = DEST / s.name
        state = "바꿈" if d.exists() else "새로"
        if d.is_symlink() or d.is_file():
            print(f"건너뜀  {s.name}  (같은 이름의 링크나 파일이 있습니다: {d})")
            continue
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(s, d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"{state}  {s.name}")
    build = HERE / "BUILD.txt"
    if build.is_file():
        shutil.copyfile(build, DEST / "감사세팅-setup" / "BUILD.txt")
    print(f"\n스킬 {len(skills)}개를 {DEST} 에 두었습니다. Claude 앱을 다시 열어 주십시오.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
