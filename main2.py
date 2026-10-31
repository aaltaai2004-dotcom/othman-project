
import flet as ft


def main(page: ft.Page):

    # ==========================================
    # APP SETTINGS
    # ==========================================

    page.title = "Game Streaming"
    page.bgcolor = "#0B1020"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    PURPLE = "#7657F6"
    BG = "#0B1020"
    CARD = "#172139"
    WHITE = "#FFFFFF"
    GREY = "#929BB0"
    RED = "#FF5577"

    # ==========================================
    # DATABASE (TEMPORARY)
    # ==========================================

    users = {}
    current_user = {
        "name": "GamePlayer",
        "email": "",
        "followers": 0,
        "following": [],
        "moderators": [],
        "is_live": False,
    }

    videos = [
        {
            "id": 1,
            "owner": "GamePlayer",
            "description": "Welcome to Game Streaming! 🎮",
            "hashtags": "#Gaming #GameStreaming",
            "likes": 0,
            "comments": [],
            "liked": False,
        },
        {
            "id": 2,
            "owner": "DragonPlayer",
            "description": "Epic gaming moments 🔥",
            "hashtags": "#DragonBall #Gaming",
            "likes": 0,
            "comments": [],
            "liked": False,
        },
        {
            "id": 3,
            "owner": "ProGamer",
            "description": "Let's play together!",
            "hashtags": "#Games #Pro",
            "likes": 0,
            "comments": [],
            "liked": False,
        },
    ]

    selected_video = 0
    current_tab = "لك"

    # ==========================================
    # HELPER FUNCTIONS
    # ==========================================

    def render(content):

        page.controls.clear()

        page.add(
            ft.Container(
                content=content,
                bgcolor=BG,
                expand=True,
                padding=12,
            )
        )

        page.update()

    def message(text):

        page.open(
            ft.SnackBar(
                content=ft.Text(text)
            )
        )

    def title(text, size=22):

        return ft.Text(
            text,
            size=size,
            weight=ft.FontWeight.BOLD,
            color=WHITE,
        )

    def small_text(text):

        return ft.Text(
            text,
            size=12,
            color=GREY,
        )

    def circle_button(icon, callback, color=WHITE):

        return ft.IconButton(
            icon=icon,
            icon_color=color,
            on_click=callback,
        )

    # ==========================================
    # BOTTOM NAVIGATION
    # ==========================================

    def bottom_navigation(active="home"):

        def nav_item(icon, name, callback):

            return ft.Column(
                [
                    ft.IconButton(
                        icon=icon,
                        icon_color=PURPLE if active == name else GREY,
                        icon_size=25,
                        on_click=callback,
                    ),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        return ft.Container(
            content=ft.Row(
                [
                    nav_item(ft.Icons.HOME, "home", feed_page),
                    nav_item(ft.Icons.GROUP, "friends", friends_page),
                    nav_item(ft.Icons.ADD_CIRCLE, "upload", upload_page),
                    nav_item(ft.Icons.CHAT, "messages", messages_page),
                    nav_item(ft.Icons.PERSON, "profile", profile_page),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            border=ft.Border(
                top=ft.BorderSide(1, "#28334B")
            ),
            padding=5,
        )

    # ==========================================
    # LOGIN
    # ==========================================

    def login_page(e=None):

        email = ft.TextField(
            label="البريد الإلكتروني",
            border_radius=12,
        )

        password = ft.TextField(
            label="كلمة المرور",
            password=True,
            can_reveal_password=True,
            border_radius=12,
        )

        error = ft.Text(color=RED, size=12)

        def login(e):

            if not email.value or not password.value:
                error.value = "يرجى ملء جميع الحقول"
                page.update()
                return

            if email.value not in users:
                error.value = "الحساب غير موجود"
                page.update()
                return

            if users[email.value]["password"] != password.value:
                error.value = "كلمة المرور غير صحيحة"
                page.update()
                return

            current_user["name"] = users[email.value]["name"]
            current_user["email"] = email.value

            feed_page()

        render(
            ft.Column(
                [
                    ft.Container(height=65),

                    ft.Icon(
                        ft.Icons.SPORTS_ESPORTS,
                        color=PURPLE,
                        size=75,
                    ),

                    title("Game Streaming", 29),
                    small_text("Your gaming community"),

                    ft.Container(height=25),

                    title("تسجيل الدخول", 22),

                    email,
                    password,

                    ft.Button(
                        content="تسجيل الدخول",
                        bgcolor=PURPLE,
                        color=WHITE,
                        width=350,
                        height=50,
                        on_click=login,
                    ),

                    error,

                    ft.TextButton(
                        content="إنشاء حساب جديد",
                        on_click=signup_page,
                    ),

                    ft.Container(expand=True),

                    small_text("Game Streaming © 2026"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                expand=True,
            )
        )

    # ==========================================
    # SIGN UP
    # ==========================================

    def signup_page(e=None):

        email = ft.TextField(
            label="البريد الإلكتروني",
            border_radius=12,
        )

        password = ft.TextField(
            label="كلمة المرور",
            password=True,
            can_reveal_password=True,
            border_radius=12,
        )

        name = ft.TextField(
            label="اسم المستخدم",
            border_radius=12,
        )

        error = ft.Text(color=RED, size=12)

        def register(e):

            if not email.value or not password.value or not name.value:
                error.value = "يرجى ملء جميع الحقول"
                page.update()
                return

            if "@" not in email.value:
                error.value = "البريد الإلكتروني غير صحيح"
                page.update()
                return

            if email.value in users:
                error.value = "هذا الحساب موجود"
                page.update()
                return

            users[email.value] = {
                "password": password.value,
                "name": name.value,
                "followers": 0,
                "following": [],
            }

            current_user["name"] = name.value
            current_user["email"] = email.value

            feed_page()

        render(
            ft.Column(
                [
                    ft.Container(height=70),

                    ft.Icon(
                        ft.Icons.PERSON_ADD,
                        size=60,
                        color=PURPLE,
                    ),

                    title("إنشاء حساب جديد"),

                    email,
                    password,
                    name,

                    ft.Button(
                        content="إنشاء الحساب",
                        bgcolor=PURPLE,
                        color=WHITE,
                        width=350,
                        height=50,
                        on_click=register,
                    ),

                    error,

                    ft.TextButton(
                        content="لدي حساب بالفعل",
                        on_click=login_page,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                expand=True,
            )
        )

    # ==========================================
    # FEED
    # ==========================================

    def feed_page(e=None):

        video = videos[selected_video]

        def change_video(direction):

            global selected_video

            selected_video = (
                selected_video + direction
            ) % len(videos)

            feed_page()

        def toggle_like(e):

            if video["liked"]:
                video["likes"] -= 1
                video["liked"] = False
            else:
                video["likes"] += 1
                video["liked"] = True

            feed_page()

        def open_comments(e):

            comments_page(video)

        def share_video(e):

            link = (
                "https://gamestreaming.example/video/"
                + str(video["id"])
            )

            render(
                ft.Column(
                    [
                        circle_button(
                            ft.Icons.ARROW_BACK,
                            feed_page,
                        ),

                        title("مشاركة الفيديو"),

                        ft.Container(
                            content=ft.Text(
                                link,
                                selectable=True,
                            ),
                            bgcolor=CARD,
                            padding=15,
                            border_radius=12,
                        ),

                        ft.Button(
                            content="نسخ الرابط",
                            icon=ft.Icons.COPY,
                            bgcolor=PURPLE,
                            color=WHITE,
                            on_click=lambda e: (
                                page.set_clipboard(link),
                                message("تم نسخ الرابط"),
                            ),
                        ),

                        ft.Text(
                            "يمكن مشاركة الرابط بعد ربط خدمة استضافة الفيديو.",
                            color=GREY,
                        ),
                    ],
                    expand=True,
                )
            )

        def follow_owner(e):

            owner = video["owner"]

            if owner == current_user["name"]:
                message("هذا حسابك")
                return

            if owner in current_user["following"]:
                current_user["following"].remove(owner)
                message("تم إلغاء المتابعة")
            else:
                current_user["following"].append(owner)
                message("أصبحت تتابع " + owner)

            feed_page()

        def change_tab(tab):

            global current_tab
            current_tab = tab
            feed_page()

        # VIDEO AREA

        video_area = ft.Container(
            expand=True,
            bgcolor="#202B43",
            border_radius=18,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.PLAY_CIRCLE,
                        size=85,
                        color=WHITE,
                    ),

                    title("GAME VIDEO", 20),

                    small_text("Video player placeholder"),

                    ft.Row(
                        [
                            circle_button(
                                ft.Icons.KEYBOARD_ARROW_UP,
                                lambda e: change_video(-1),
                            ),

                            circle_button(
                                ft.Icons.KEYBOARD_ARROW_DOWN,
                                lambda e: change_video(1),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # RIGHT ACTIONS

        actions = ft.Column(
            [
                ft.CircleAvatar(
                    content=ft.Icon(
                        ft.Icons.PERSON,
                        color=WHITE,
                    ),
                    bgcolor=PURPLE,
                    radius=23,
                ),

                circle_button(
                    ft.Icons.PERSON_ADD,
                    follow_owner,
                ),

                ft.IconButton(
                    icon=(
                        ft.Icons.FAVORITE
                        if video["liked"]
                        else ft.Icons.FAVORITE_BORDER
                    ),
                    icon_color=RED if video["liked"] else WHITE,
                    icon_size=30,
                    on_click=toggle_like,
                ),

                small_text(str(video["likes"])),

                circle_button(
                    ft.Icons.COMMENT,
                    open_comments,
                ),

                small_text(str(len(video["comments"]))),

                circle_button(
                    ft.Icons.SHARE,
                    share_video,
                ),

                small_text("مشاركة"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
        )

        # VIDEO INFORMATION

        information = ft.Column(
            [
                ft.Text(
                    "@" + video["owner"],
                    weight=ft.FontWeight.BOLD,
                    size=15,
                ),

                ft.Text(
                    video["description"],
                    size=14,
                ),

                ft.Text(
                    video["hashtags"],
                    color="#A78BFA",
                    size=12,
                ),
            ],
            spacing=5,
        )

        # TOP BAR

        top = ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.SPORTS_ESPORTS,
                            color=PURPLE,
                            size=28,
                        ),
                        title("Game Streaming", 17),
                    ],
                ),

                ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    icon_color=WHITE,
                    on_click=search_page,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        tabs = ft.Row(
            [
                ft.TextButton(
                    content="أصدقاؤك",
                    on_click=lambda e: change_tab("أصدقاؤك"),
                    style=ft.ButtonStyle(
                        color=PURPLE if current_tab == "أصدقاؤك" else GREY
                    ),
                ),

                ft.TextButton(
                    content="لك",
                    on_click=lambda e: change_tab("لك"),
                    style=ft.ButtonStyle(
                        color=PURPLE if current_tab == "لك" else GREY
                    ),
                ),

                ft.TextButton(
                    content="أتابعهم",
                    on_click=lambda e: change_tab("أتابعهم"),
                    style=ft.ButtonStyle(
                        color=PURPLE if current_tab == "أتابعهم" else GREY
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        render(
            ft.Column(
                [
                    top,
                    tabs,

                    ft.Row(
                        [
                            video_area,
                            actions,
                        ],
                        expand=True,
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),

                    information,

                    bottom_navigation("home"),
                ],
                expand=True,
                spacing=8,
            )
        )

    # ==========================================
    # COMMENTS PAGE
    # ==========================================

    def comments_page(video):

        comment_input = ft.TextField(
            hint_text="اكتب تعليقك...",
            border_radius=20,
            expand=True,
        )

        def add_comment(e):

            text = comment_input.value.strip()

            if not text:
                return

            video["comments"].append(
                {
                    "user": current_user["name"],
                    "text": text,
                }
            )

            comment_input.value = ""
            comments_page(video)

        def delete_comment(index):

            if video["comments"][index]["user"] != current_user["name"]:
                message("لا يمكنك حذف تعليق شخص آخر")
                return

            video["comments"].pop(index)
            comments_page(video)

        def translate_comment(comment):

            comment["translated"] = not comment.get(
                "translated", False
            )

            comments_page(video)

        comment_controls = []

        for index, comment in enumerate(video["comments"]):

            comment_controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Icon(ft.Icons.PERSON),
                                        radius=17,
                                        bgcolor=PURPLE,
                                    ),

                                    ft.Text(
                                        comment["user"],
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    ft.Container(expand=True),

                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=RED,
                                        on_click=lambda e, i=index: delete_comment(i),
                                    ),
                                ],
                            ),

                            ft.Text(comment["text"]),

                            ft.TextButton(
                                content=(
                                    "إخفاء الترجمة"
                                    if comment.get("translated")
                                    else "ترجمة التعليق"
                                ),
                                on_click=lambda e, c=comment: translate_comment(c),
                            ),

                            ft.Text(
                                "Translation requires connecting a translation service."
                                if comment.get("translated")
                                else "",
                                color=GREY,
                                size=11,
                            ),
                        ],
                        spacing=3,
                    ),
                    bgcolor=CARD,
                    padding=10,
                    border_radius=12,
                )
            )

        render(
            ft.Column(
                [
                    ft.Row(
                        [
                            circle_button(
                                ft.Icons.ARROW_BACK,
                                feed_page,
                            ),

                            title("التعليقات"),

                            ft.Container(expand=True),

                            small_text(str(len(video["comments"]))),
                        ]
                    ),

                    ft.Column(
                        comment_controls,
                        spacing=10,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),

                    ft.Row(
                        [
                            comment_input,

                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                icon_color=PURPLE,
                                on_click=add_comment,
                            ),
                        ]
                    ),
                ],
                expand=True,
            )
        )

    # ==========================================
    # SEARCH
    # ==========================================

    def search_page(e=None):

        search_input = ft.TextField(
            hint_text="ابحث عن لاعب أو حساب...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=15,
        )

        results = ft.Column(spacing=10, expand=True)

        def search(e=None):

            results.controls.clear()

            query = search_input.value.lower().strip()

            for account_email, account in users.items():

                name = account["name"]

                if query and query not in name.lower():
                    continue

                results.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.CircleAvatar(
                                    content=ft.Icon(ft.Icons.PERSON),
                                    bgcolor=PURPLE,
                                ),

                                ft.Column(
                                    [
                                        ft.Text(
                                            name,
                                            weight=ft.FontWeight.BOLD,
                                        ),

                                        small_text("Game Streaming user"),
                                    ],
                                    expand=True,
                                    spacing=3,
                                ),

                                ft.Button(
                                    content=(
                                        "متابَع"
                                        if name in current_user["following"]
                                        else "متابعة"
                                    ),
                                    bgcolor=PURPLE,
                                    color=WHITE,
                                    on_click=lambda e, n=name: toggle_follow(n),
                                ),
                            ]
                        ),
                        bgcolor=CARD,
                        padding=12,
                        border_radius=12,
                    )
                )

            if not results.controls:
                results.controls.append(
                    small_text("لا توجد حسابات مطابقة")
                )

            page.update()

        search_input.on_change = search

        render(
            ft.Column(
                [
                    ft.Row(
                        [
                            circle_button(ft.Icons.ARROW_BACK, feed_page),
                            title("البحث"),
                        ]
                    ),

                    search_input,
                    results,
                    bottom_navigation(),
                ],
                expand=True,
            )
        )

        search()

    # ==========================================
    # FOLLOW SYSTEM
    # ==========================================

    def toggle_follow(name):

        if name == current_user["name"]:
            message("لا يمكنك متابعة نفسك")
            return

        if name in current_user["following"]:
            current_user["following"].remove(name)
            message("تم إلغاء المتابعة")
        else:
            current_user["following"].append(name)
            message("تمت المتابعة")

        search_page()

    # ==========================================
    # FRIENDS
    # ==========================================

    def friends_page(e=None):

        following_controls = []

        for name in current_user["following"]:

            following_controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON),
                                bgcolor=PURPLE,
                            ),

                            ft.Text(name, expand=True),

                            ft.TextButton(
                                content="إلغاء المتابعة",
                                on_click=lambda e, n=name: unfollow(n),
                            ),
                        ]
                    ),
                    bgcolor=CARD,
                    padding=12,
                    border_radius=12,
                )
            )

        render(
            ft.Column(
                [
                    title("الأصدقاء"),

                    small_text("الأشخاص الذين تتابعهم"),

                    ft.Column(
                        following_controls,
                        spacing=10,
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                    ),

                    bottom_navigation("friends"),
                ],
                expand=True,
            )
        )

    def unfollow(name):

        if name in current_user["following"]:
            current_user["following"].remove(name)

        friends_page()

    # ==========================================
    # UPLOAD
    # ==========================================

    def upload_page(e=None):

        description = ft.TextField(
            label="وصف الفيديو",
            multiline=True,
            min_lines=2,
        )

        hashtags = ft.TextField(
            label="الهاشتاقات",
        )

        def publish(e):

            if not description.value:
                message("اكتب وصف الفيديو أولاً")
                return

            videos.insert(
                0,
                {
                    "id": len(videos) + 1,
                    "owner": current_user["name"],
                    "description": description.value,
                    "hashtags": hashtags.value or "#Gaming",
                    "likes": 0,
                    "comments": [],
                    "liked": False,
                },
            )

            global selected_video
            selected_video = 0

            message("تم إنشاء مقطع تجريبي")
            feed_page()

        render(
            ft.Column(
                [
                    title("إضافة فيديو"),

                    ft.Container(height=20),

                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.VIDEO_LIBRARY,
                                    size=65,
                                    color=PURPLE,
                                ),

                                title("اختر فيديو", 18),

                                small_text(
                                    "سيتم ربط معرض الهاتف في المرحلة التالية"
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=CARD,
                        padding=30,
                        border_radius=15,
                        alignment=ft.Alignment.CENTER,
                    ),

                    description,
                    hashtags,

                    ft.Button(
                        content="نشر المقطع التجريبي",
                        bgcolor=PURPLE,
                        color=WHITE,
                        width=350,
                        on_click=publish,
                    ),

                    bottom_navigation("upload"),
                ],
                expand=True,
                spacing=15,
            )
        )

    # ==========================================
    # PROFILE
    # ==========================================

    def profile_page(e=None):

        following_count = len(current_user["following"])

        my_videos = [
            video for video in videos
            if video["owner"] == current_user["name"]
        ]

        render(
            ft.Column(
                [
                    ft.Row(
                        [
                            title("الملف الشخصي"),
                            ft.Container(expand=True),
                            circle_button(
                                ft.Icons.SETTINGS,
                                lambda e: settings_page(),
                            ),
                        ]
                    ),

                    ft.Container(height=15),

                    ft.CircleAvatar(
                        content=ft.Icon(
                            ft.Icons.PERSON,
                            size=50,
                        ),
                        radius=50,
                        bgcolor=PURPLE,
                    ),

                    title(current_user["name"], 23),

                    small_text("Gaming Creator 🎮"),

                    ft.Row(
                        [
                            profile_stat(
                                len(my_videos),
                                "المقاطع",
                            ),

                            profile_stat(
                                current_user["followers"],
                                "المتابعون",
                            ),

                            profile_stat(
                                following_count,
                                "أتابع",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),

                    ft.Divider(color="#28334B"),

                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.SENSORS,
                                    color=RED,
                                    size=45,
                                ),

                                title("ابدأ بثاً مباشراً", 20),

                                small_text(
                                    "تواصل مع اللاعبين في الوقت الحقيقي"
                                ),

                                ft.Button(
                                    content="بدء البث المباشر",
                                    bgcolor=RED,
                                    color=WHITE,
                                    on_click=start_live,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        bgcolor=CARD,
                        padding=25,
                        border_radius=18,
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                    ),

                    ft.TextButton(
                        content="تسجيل الخروج",
                        on_click=logout,
                    ),

                    bottom_navigation("profile"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=12,
            )
        )

    def profile_stat(number, label):

        return ft.Column(
            [
                title(str(number), 20),
                small_text(label),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ==========================================
    # LIVE STREAM
    # ==========================================

    live_hearts = 0
    live_viewers = 1
    live_comments = []
    live_active = False

    def start_live(e=None):

        global live_hearts, live_viewers, live_comments, live_active

        live_hearts = 0
        live_viewers = 1
        live_comments = []
        live_active = True

        current_user["is_live"] = True

        live_page()

    def live_page(e=None):

        live_message = ft.TextField(
            hint_text="اكتب رسالة...",
            expand=True,
            border_radius=20,
        )

        chat_list = ft.Column(
            spacing=5,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        def refresh_chat():

            chat_list.controls.clear()

            for comment in live_comments:

                chat_list.controls.append(
                    ft.Container(
                        content=ft.Text(
                            comment["user"] + ": " + comment["text"],
                            color=WHITE,
                            size=12,
                        ),
                        bgcolor="#26334C",
                        padding=7,
                        border_radius=10,
                    )
                )

        def send_message(e):

            if not live_message.value:
                return

            live_comments.append(
                {
                    "user": current_user["name"],
                    "text": live_message.value,
                }
            )

            live_message.value = ""

            refresh_chat()
            page.update()

        def send_heart(e):

            global live_hearts

            live_hearts += 1

            heart_count.value = str(live_hearts)
            page.update()

        def end_live(e):

            global live_active

            live_active = False
            current_user["is_live"] = False

            message("انتهى البث المباشر")
            profile_page()

        heart_count = title("❤️ 0", 23)

        def manage_moderators(e=None):

            moderator_input = ft.TextField(
                label="اسم المستخدم لإضافته كمشرف"
            )

            def add_moderator(e):

                name = moderator_input.value.strip()

                if not name:
                    return

                if name == current_user["name"]:
                    message("لا يمكنك تعيين نفسك مشرفاً")
                    return

                if name not in current_user["moderators"]:
                    current_user["moderators"].append(name)

                message("تمت إضافة المشرف")
                manage_moderators()

            moderator_list = ft.Column()

            for name in current_user["moderators"]:

                moderator_list.controls.append(
                    ft.Row(
                        [
                            ft.Text(name, expand=True),

                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=RED,
                                on_click=lambda e, n=name: remove_moderator(n),
                            ),
                        ]
                    )
                )

            render(
                ft.Column(
                    [
                        ft.Row(
                            [
                                circle_button(
                                    ft.Icons.ARROW_BACK,
                                    live_page,
                                ),

                                title("إدارة المشرفين"),
                            ]
                        ),

                        moderator_input,

                        ft.Button(
                            content="إضافة مشرف",
                            bgcolor=PURPLE,
                            color=WHITE,
                            on_click=add_moderator,
                        ),

                        title("المشرفون الحاليون", 17),

                        moderator_list,
                    ],
                    expand=True,
                )
            )

        def remove_moderator(name):

            if name in current_user["moderators"]:
                current_user["moderators"].remove(name)

            manage_moderators()

        refresh_chat()

        render(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CIRCLE,
                                color=RED,
                                size=12,
                            ),

                            title("LIVE", 18),

                            ft.Container(expand=True),

                            small_text(
                                "مشاهدون: " + str(live_viewers)
                            ),

                            circle_button(
                                ft.Icons.GROUP,
                                manage_moderators,
                            ),
                        ]
                    ),

                    ft.Container(
                        content=ft.Column(
                            [
                                ft.CircleAvatar(
                                    content=ft.Icon(
                                        ft.Icons.PERSON,
                                        size=45,
                                    ),
                                    radius=45,
                                    bgcolor=PURPLE,
                                ),

                                title(current_user["name"], 22),

                                small_text("البث المباشر للألعاب"),

                                ft.Button(
                                    content="متابعة",
                                    bgcolor=PURPLE,
                                    color=WHITE,
                                ),

                                ft.Container(height=35),

                                ft.Icon(
                                    ft.Icons.VIDEOCAM,
                                    size=75,
                                    color=GREY,
                                ),

                                title("LIVE STREAM", 20),

                                small_text(
                                    "مكان عرض بث الكاميرا أو اللعبة"
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor="#172139",
                        border_radius=18,
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                    ),

                    heart_count,

                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.FAVORITE,
                                icon_color=RED,
                                icon_size=38,
                                on_click=send_heart,
                            ),

                            small_text("اضغط لإرسال القلوب"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Container(
                        content=chat_list,
                        height=150,
                        bgcolor=CARD,
                        padding=8,
                        border_radius=12,
                    ),

                    ft.Row(
                        [
                            live_message,

                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                icon_color=PURPLE,
                                on_click=send_message,
                            ),
                        ]
                    ),

                    ft.Button(
                        content="إنهاء البث",
                        bgcolor=RED,
                        color=WHITE,
                        width=350,
                        on_click=end_live,
                    ),
                ],
                expand=True,
                spacing=8,
            )
        )

    # ==========================================
    # MESSAGES
    # ==========================================

    def messages_page(e=None):

        render(
            ft.Column(
                [
                    title("الرسائل"),

                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.CHAT_BUBBLE_OUTLINE,
                                    size=55,
                                    color=PURPLE,
                                ),

                                title("لا توجد محادثات", 18),

                                small_text(
                                    "ستظهر محادثاتك هنا"
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                    ),

                    bottom_navigation("messages"),
                ],
                expand=True,
            )
        )

    # ==========================================
    # SETTINGS
    # ==========================================

    def settings_page():

        render(
            ft.Column(
                [
                    ft.Row(
                        [
                            circle_button(
                                ft.Icons.ARROW_BACK,
                                profile_page,
                            ),

                            title("الإعدادات"),
                        ]
                    ),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON),
                        title=ft.Text("الحساب"),
                        subtitle=ft.Text(current_user["name"]),
                    ),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.NOTIFICATIONS),
                        title=ft.Text("الإشعارات"),
                        subtitle=ft.Text("قريباً"),
                    ),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SECURITY),
                        title=ft.Text("الخصوصية والأمان"),
                        subtitle=ft.Text("قريباً"),
                    ),

                    ft.Button(
                        content="تسجيل الخروج",
                        bgcolor=RED,
                        color=WHITE,
                        on_click=logout,
                    ),
                ],
                expand=True,
            )
        )

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(e):

        current_user["name"] = "GamePlayer"
        current_user["email"] = ""
        current_user["following"] = []

        login_page()

    # ==========================================
    # START
    # ==========================================

    login_page()


ft.run(main, view=ft.AppView.WEB_BROWSER)
