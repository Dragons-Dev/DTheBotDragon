import discord


def rules() -> list[discord.Embed]:
    introduction = discord.Embed(
        title="Willkommen auf dem Dragons Discord!",
        description="Finde Freunde, hab Spaß, lern etwas oder sei einfach mit dabei.\n\nWenn du deine Freunde ebenfalls auf den Server einladen möchtest, dann verwende bitte den Folgenden link: https://discord.com/invite/bd8vUQd\n\nBitte lies dir die Nachfolgende Regeln genau durch oder lies dir die Zusammenfassung unserer Regeln in dem für dich erstellten Channel durch. Du findest diesen Channel ganz unten und kannst dort unserem Regelwerk zustimmen. Nach dem Zustimmen bekommst du die Rolle <@&876927534904803398>. Mit dieser Rolle erhälts du die Berechtigung die meisten Kanäle einzusehen und kannst damit auch nach dem Regelwerk belangt werden. Wenn du die Regeln erneut nachlesen möchtest kannst du das jeder Zeit in diesem Channel (<#705800487517028493>) tun. Weitere Rollen kannst du dir nach bedarf im <#878281562637074432> selbst hinzufügen oder dir werden höhere Rechte durch <@&876927201390522429> eingeräumt.\n\nWir wünschen dir einen angenehmen Aufenthalt auf unserem Discord Server und <@&877227680867713024> stehen dir bei Fragen jeder Zeit zur Verfügung. Wir bitten dich jedoch Mitglieder von <@&876927201390522429> nicht unnötig zu belästigen, sonst ist mit Konsequenzen zu rechnen.",
        color=4653192,
    ).set_author(
        name="Ultimate Dragons",
        url="https://discord.com/invite/bd8vUQd",
        icon_url="https://cdn.discordapp.com/attachments/962327039053033472/962327055066861638/dragon.jpg",
    )
    rule1 = discord.Embed(
        title="Der nachfolgende Text beinhaltet die Regel dieses Discords",
        description="__**§1 Moderation Regelungen**__\n**[I.]** Aussagen von <@&876927201390522429> ist Glauben zu schenken .\n**[II.]** Verwarnungen von <@&876927201390522429> sind so hinzunehmen.\n**[III.]** Entscheidungen jeglicher Art von <@&876927201390522429> ist Folge zu leisten.\n**[IV.]** Entscheidung der <@&877227680867713024>können an gestritten werden.\n**[V.]** <@&876927201390522429> sind **NICHT** dazu angehalten jeder Anfrage nachzukommen.",
        color=1376000,
    )
    rule2 = discord.Embed(
        description="__**§2 Regel Gültigkeit**__\n**[I.]** Den Folgenden Regeln und Bestimmungen wird mit dem erlangen des Ranges <@&876927534904803398>ausnahmslos zugestimmt.\n**[II.]** Bei Verletzung des Regelwerkes wird wie in **§4** beschrieben geahndet.\n**[III.]** Alle Änderungen des Regelwerkes werden im Regelwerk bekannt gegeben und denen ist auch **unverzüglich** Folge zu leisten.\n**[IV.]** Alle Regelverstöße sind **NICHT** durch Wörter wie z.B.: KAPPA o.Ä. außer Kraft zu setzen und werden dementsprechend geahndet. \nSetzt dementsprechend Ironie in einem Verständlichen Maße ein und stellt sicher das eure Aussagen so verstanden werden wie ihr sie meint.",
        color=1376000,
    )
    rule3 = discord.Embed(
        description="__**§3 Regeln**__\n**[I.]** Alle Verstöße gegen die nachfolgenden Regeln ist von @everyone dem <@861323291716354058> per Direktnachricht zu melden.\nWenn dies nicht geschieht, wird dieser Verstoß gegen diese Regel wie in **§4 [II]** geahndet. Bei Meldungen ist eine eventuell anschließende verpflichtende Besprechung **NICHT** auszuschließen.\n**[II.]** Sexismus, Sexuelle Belästigung, Mobbing, Antisemitismus, Politische Denkrichtungen, Beleidigungen etc. haben auf diesem Discord nichts verloren, wenn sie nichts zu einer sachlichen Diskussion gehören.\n**[III.]** Wenn sich jemand eine nicht seinem Alter entsprechende Rolle zuteilt/zuteilen lässt und dies an das Serviceteam herangetragen wird stellt das einen Regelverstoß dar der dementsprechend geahndet wir siehe **§4 [IV]**.\n**[IV]** Werbung ist generell außerhalb der dafür vorgesehenen Channel verboten **§4 [V]** geahndet.\n**[V.]** Spam, Links, ASCII Emojis o.Ä. sind zu vermeiden.\n**[VI.]** Emote spam ist ebenfalls untersagt! Hierbei bitten wir den **§4 [VI]** zu beachten.\n**[VII.]** Jegliche Emotes o.Ä. die Auslöser für gewisse Krankheiten darstellen könnten sind verboten.",
        color=1376000,
    )
    rule4 = discord.Embed(
        description="__**§4 Ahndung der Regelverstöße**__\n**[I.]** Die Folgenden Ahndungen sind nur Vorschläge und können von <@&876927201390522429> nach Bedarf abgeändert werden.\n**[II.]** Zu **§3 [I]** dieser Regelverstoß wird genauso bestraft wie auch der Verstoß gegen die Regel.\n**[III.]** Zu **§3 [II]** hier wird mit einer Verwarnung begonnen jedoch kann es auch nach Anzahl und schwere des Regelverstoßes bis zu einem **PERMANENTEN** **AUSCHLUSS** von diesem Discord führen.\n**[IV.]** Zu **§3 [III]** in diesem Fall wird die Rolle weggenommen und das vergehen mit einem Timeout bestraft.\n**[V.]** Zu **§3 [IV]** bei einem solchen verstoß muss mit einer Verwarnung in leichten Fällen gerechnet werden und in schweren Fällen ebenfalls mit einem Verweis von diesem Discord.\n**[VI.]** Zu **§3 [V]** und **§3 [VI]** kann von <@861323291716354058> oder <@&876927201390522429> geahndet werden. Hierbei ist zu beachten das der Bot sehr schnell reagiert und sofort ohne Vorwarnung Timeouts verteilt und demjenigen dies auch mitteilt. Wir garantieren nicht für eine 100% Funktion des BOTs und bitten daher um Meldung bei einem solchen Problem.\n**[VII.]** Zu **§3 [VII]** dies wird je nach fall stark oder schwach geahndet aber in jenem falle ist es eine Gefährdung der Gesundheit eines Nutzers wodurch dabei mit schweren Strafen zu rechnen ist.",
        color=1376000,
    )
    disclaimer = discord.Embed(
        description="Alle Arten der Überprüfung stehen <@&695660961201258689> zur Verfügung.\nAlle Verstöße werden genauestens Protokolliert! Ein nachträgliches anfechten nach Fällung einer Entscheidung ist **ausgeschlossen**.",
        color=7602176,
    )
    disclaimer.add_field(
        name="Ultimate Dragons",
        value="<@511219492332896266>\n<@622130169657688074>\n<@579395061222080563>",
        inline=True,
    )
    disclaimer.add_field(
        name="Mod Dragons",
        value="<@861323291716354058>\n<@239151351341383680>\n<@701027384840814623>",
        inline=True,
    )
    return [introduction, rule1, rule2, rule3, rule4, disclaimer]


def random_node_idents() -> list[str]:
    words = [
        "apple",
        "bacon",
        "beef",
        "bird",
        "bread",
        "carrot",
        "cherry",
        "chicken",
        "coffee",
        "corn",
        "deer",
        "diamond",
        "disk",
        "duck",
        "fearless",
        "feather",
        "flower",
        "garden",
        "garlic",
        "ghost",
        "heart",
        "honey",
        "horse",
        "imagination",
        "laboratory",
        "leaf",
        "magic",
        "mango",
        "night",
        "north",
        "onion",
        "paper",
        "peach",
        "piano",
        "pineapple",
        "potato",
        "power",
        "rabbit",
        "racoon",
        "reality",
        "rice",
        "river",
        "salad",
        "smoke",
        "snail",
        "stranger",
        "tale",
        "torch",
        "watermelon",
        "wave",
        "wheat",
        "wire",
        "wood",
    ]
    return words
