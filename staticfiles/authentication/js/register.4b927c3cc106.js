usernameField = document.querySelector('#id_username')

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    console.log(usernameVal)

    if (usernameVal > 0) {
        fetch("/authentication/validate/", {
                method: "POST",
                body: JSON.stringify({ username: usernameVal }),
            }).then(response => response.json())
            .then(data => {
                console.log(data);
                /*  if (data.username_error) {
                      usernameField.classList.add('is-invalid')
                  }*/
            });
    }
})