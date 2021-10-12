const usernameField = document.querySelector("#id_username");
const userDiv = document.querySelector("#div_id_username")

let tag = document.createElement("span");
tag.classList.add("text-danger", "font-weight-bold")


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value; //equals the value the user types
    usernameField.classList.remove("is-invalid");


    if (usernameVal.length > 0) {
        tag.remove()
        fetch("/authentication/validate/", {
                body: JSON.stringify({ username: usernameVal }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                userDiv.classList.remove("is-invalid")
                if (data.username_exists) {
                    usernameField.classList.add("is-invalid");
                    tag.innerHTML = "username already exists"
                    userDiv.appendChild(tag);

                }
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    tag.innerHTML = "username should contain alphanumeric characters only"
                    userDiv.appendChild(tag)
                }

            });
    }
});