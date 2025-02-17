import streamlit as st
import base64

# Initialize session state variables
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
if "selected_hobbies" not in st.session_state:
    st.session_state.selected_hobbies = set()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "active_community_chat" not in st.session_state:
    st.session_state.active_community_chat = None
if "messages" not in st.session_state:
    st.session_state.messages = {}
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "", "username": "", "bio": "", "image": None, "image_size": 150}

# Helper functions
def get_messages(community_id):
    return st.session_state.messages.get(community_id, [])

def send_message(community_id, message):
    if community_id not in st.session_state.messages:
        st.session_state.messages[community_id] = []
    st.session_state.messages[community_id].append(message)

# Sidebar Navigation (Reordered)
st.sidebar.title("Locali Navigation")
st.sidebar.markdown("**Sections**")
if st.sidebar.button("Home"):
    st.session_state.active_tab = "Home"
    st.session_state.submitted = False
if st.sidebar.button("Your Profile"):
    st.session_state.active_tab = "Your Profile"
    st.session_state.submitted = False
if st.sidebar.button("Hobby Matching"):
    st.session_state.active_tab = "Hobby Matching"
    st.session_state.submitted = False
if st.sidebar.button("Explore"):
    st.session_state.active_tab = "Explore"
    st.session_state.submitted = False
if st.sidebar.button("Chat"):
    st.session_state.active_tab = "Chat"
    st.session_state.submitted = False

tabs = st.session_state.active_tab

# Home Page
if tabs == "Home":
    st.title("Welcome to Locali")
    st.subheader("Your Gateway to Hobby Matching and Community Discovery")
    st.write("Locali is designed to help you find people who share your passions. Whether you’re into cooking, photography, gaming, or exploring the great outdoors, Locali connects you with communities and events that match your interests.")
    st.image("/Users/timonwin/Downloads/StreamLitApp/images/locali_home.jpg", use_container_width=True)
    st.write("""
        ### What can you do with Locali?
        - **Find Matches:** Select hobbies to discover groups with shared interests.
        - **Personalize Your Profile:** Tell us about yourself so we can make better suggestions.
        - **Explore Communities:** Discover trending groups and events near you.
    """)
    st.write("Join Locali today and start building connections with like-minded people.")

# Hobby Matching Page
elif tabs == "Hobby Matching":
    st.title("Find Your Hobby Match")
    st.write("Select the hobbies that interest you and see what communities are out there.")
    
    # List of hobbies (expanded)
    hobby_list = [
        "📷 Photography",
        "🥾 Hiking",
        "🍳 Cooking",
        "🎵 Music",
        "🎮 Gaming",
        "📚 Reading",
        "🏋️ Fitness",
        "🎨 Art",
        "💻 Technology",
        "✈️ Travel",
        "🌱 Gardening",
        "🧶 Crafts",
        "🎨 Painting",
        "🎲 Board Games",
        "🧘 Yoga",
        "🔨 DIY Projects",
        "💃 Dancing",
        "🔭 Astronomy",
    ]
    
    # Real-time selection with tags
    col1, col2, col3 = st.columns(3)
    for i, hobby in enumerate(hobby_list):
        if (i % 3) == 0:
            with col1:
                if st.button(hobby):
                    if hobby in st.session_state.selected_hobbies:
                        st.session_state.selected_hobbies.remove(hobby)
                    else:
                        st.session_state.selected_hobbies.add(hobby)
        elif (i % 3) == 1:
            with col2:
                if st.button(hobby):
                    if hobby in st.session_state.selected_hobbies:
                        st.session_state.selected_hobbies.remove(hobby)
                    else:
                        st.session_state.selected_hobbies.add(hobby)
        else:
            with col3:
                if st.button(hobby):
                    if hobby in st.session_state.selected_hobbies:
                        st.session_state.selected_hobbies.remove(hobby)
                    else:
                        st.session_state.selected_hobbies.add(hobby)

    # Display selected hobbies
    st.write("### Selected Hobbies")
    if "selected_hobbies" not in st.session_state or not isinstance(st.session_state.selected_hobbies, set):
        st.session_state.selected_hobbies = set()

    for hobby in st.session_state.selected_hobbies.copy():
        if st.button(f"❌ {hobby}", key=f"remove_{hobby}"):
            st.session_state.selected_hobbies.remove(hobby)

    if st.button("Submit"):
        st.session_state.submitted = True

    if st.session_state.submitted:
        st.write("### Hobby Matching Confirmation")
        st.write("You selected these hobbies:")
        st.write(", ".join(st.session_state.selected_hobbies))
        st.write("**Finding communities...**")

# Profile Page
elif tabs == "Your Profile":
    st.title("Your Profile")
    st.write("Customize your profile and personalize your experience:")

    # Profile picture upload and resizing
    uploaded_image = st.file_uploader("Upload a profile picture", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        st.session_state.profile["image"] = base64.b64encode(uploaded_image.getvalue()).decode("utf-8")
    image_size = st.slider("Resize your profile picture:", 50, 200, st.session_state.profile["image_size"])
    st.session_state.profile["image_size"] = image_size

    # Show the circular profile picture preview
    if st.session_state.profile["image"]:
        st.markdown("""
        <style>
        .circle {
            width: {size}px;
            height: {size}px;
            border-radius: 50%;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .circle img {
            width: 100%;
            height: auto;
        }
        </style>
        """.format(size=image_size), unsafe_allow_html=True)

        st.markdown(
            f'<div class="circle"><img src="data:image/jpeg;base64,{st.session_state.profile["image"]}"/></div>',
            unsafe_allow_html=True
        )

    # Personal information
    name = st.text_input("Your Name:", value=st.session_state.profile["name"])
    username = st.text_input("Your Username:", value=st.session_state.profile["username"])
    bio = st.text_area("Short Bio (Tell others about yourself):", value=st.session_state.profile["bio"])

    # Save button
    if st.button("Save Profile"):
        st.session_state.profile["name"] = name
        st.session_state.profile["username"] = username
        st.session_state.profile["bio"] = bio
        st.write("Your profile has been updated!")

# Explore Page
elif tabs == "Explore":
    st.title("Explore Communities")
    st.write("Discover trending communities and events:")

    # Filter and search bar
    st.sidebar.markdown("**Filter Communities**")
    category_filter = st.sidebar.selectbox("Category", ["All", "Adventure", "Culinary", "Technology", "Art"])
    search_query = st.sidebar.text_input("Search by keyword")

    # Communities with full details
    communities = [
        {
            "name": "Adventure Seekers",
            "description": "Join a group of thrill-seekers and explorers who love outdoor adventures and pushing their limits.",
            "category": "Adventure",
            "image": "/Users/timonwin/Downloads/StreamLitApp/images/adventure_seekers.jpg",
            "details": {
                "Address": "Mountain Trailhead, Cityville",
                "Meet Frequency": "Weekly",
                "Members": 25,
                "Website": "https://example.com/adventure-seekers",
            }
        },
        {
            "name": "Gourmet Chefs",
            "description": "A community of culinary enthusiasts sharing recipes, cooking tips, and food inspiration.",
            "category": "Culinary",
            "image": "/Users/timonwin/Downloads/StreamLitApp/images/gourmet_chefs.jpg",
            "details": {
                "Address": "Cooking Studio, Foodtown",
                "Meet Frequency": "Bi-Weekly",
                "Members": 40,
                "Website": "https://example.com/gourmet-chefs",
            }
        },
        {
            "name": "Tech Enthusiasts",
            "description": "Connect with tech innovators, gadget lovers, and coding wizards who share your passion for technology.",
            "category": "Technology",
            "image": "/Users/timonwin/Downloads/StreamLitApp/images/tech_enthusiasts.jpg",
            "details": {
                "Address": "Tech Hub, Silicon City",
                "Meet Frequency": "Monthly",
                "Members": 60,
                "Website": "https://example.com/tech-enthusiasts",
            }
        },
        {
            "name": "Art Lovers",
            "description": "Discover a vibrant group of artists and art appreciators who share your creative vision.",
            "category": "Art",
            "image": "/Users/timonwin/Downloads/StreamLitApp/images/art_lovers.jpg",
            "details": {
                "Address": "Gallery District, Artsville",
                "Meet Frequency": "Every Saturday",
                "Members": 50,
                "Website": "https://example.com/art-lovers",
            }
        }
    ]

    # Filter communities by category and search query
    filtered_communities = [
        c for c in communities
        if (category_filter == "All" or c["category"] == category_filter) and
        (search_query.lower() in c["name"].lower() or search_query.lower() in c["description"].lower())
    ]

    # Display filtered communities
    for community in filtered_communities:
        with st.container():
            st.image(community["image"], use_container_width=True)
            st.subheader(community["name"])
            st.write(community["description"])
            with st.expander("More Details"):
                for key, value in community["details"].items():
                    if key == "Website":
                        st.markdown(f"[Visit {community['name']} Website]({value})")
                    else:
                        st.write(f"**{key}:** {value}")

# Chat Page
elif tabs == "Chat":
    if st.session_state.active_community_chat is None:
        st.title("Community Chat")
        st.write("Select a community to chat in:")

        communities = [
            {"id": "adventure_seekers", "name": "Adventure Seekers"},
            {"id": "gourmet_chefs", "name": "Gourmet Chefs"},
            {"id": "tech_enthusiasts", "name": "Tech Enthusiasts"},
            {"id": "art_lovers", "name": "Art Lovers"},
        ]

        for community in communities:
            if st.button(f"Join {community['name']} Chat"):
                st.session_state.active_community_chat = community["id"]

    else:
        community_id = st.session_state.active_community_chat
        st.title(f"Chatting in {community_id.capitalize()} Chat")

        st.write("### Chat History")
        messages = get_messages(community_id)
        for msg in messages:
            sender = msg.split(":", 1)[0]
            content = msg.split(":", 1)[1]
            st.markdown(f"**{sender}:** {content}")

        st.write("### New Message")
        new_message = st.text_input("Your message")
        if st.button("Send"):
            if st.session_state.profile["username"]:
                sender = st.session_state.profile["username"]
            else:
                sender = "User"
            send_message(community_id, f"{sender}: {new_message}")

        # Back button to return to chat community options
        if st.button("Back"):
            st.session_state.active_community_chat = None
