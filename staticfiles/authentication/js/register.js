const usernameField = document.querySelector("#id_username");
const userDiv = document.querySelector("#div_id_username")

usernameField.addEventListener("blur", (e) => {
    const usernameVal = e.target.value; //equals the value the user types
    usernameField.classList.remove("is-invalid");


    if (usernameVal.length > 0) {
        fetch("/authentication/validate/", {
                body: JSON.stringify({ username: usernameVal }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log(data)

                if (data.username_exists) {
                    usernameField.classList.add("is-invalid");
                    let tag = document.createElement("span")
                    let text = document.createTextNode("username already exists")
                    tag.appendChild(text)
                    userDiv.appendChild(tag)

                }
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    let tag = document.createElement("div")
                    let text = document.createTextNode("username should contain alphanumeric characters only")
                    tag.appendChild(text)
                    userDiv.appendChild(tag)

                }
                userDiv.tag.remove()

            });
    }
});