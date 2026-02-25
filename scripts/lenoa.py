embed

<drac2>
using (
    t="f60313a3-fe57-4354-8b3c-b0a8cb4c5926" # templates
)
# [T]EMPLATES

Title = t.lenoa["title"]
footer = t.command_prefix + t.lenoa["footer_postfix"] + t.credits
desc = ""

desc += f"Number of Commands Available: {len(t.commands)}\n"
for value in t.commands.values():
    if ("footer_postfix" in value):
        desc += f"{t.command_prefix} {value['footer_postfix']}\n"

</drac2>

-title "{{Title}}"
-desc "{{desc}}"
-footer "{{footer}}"