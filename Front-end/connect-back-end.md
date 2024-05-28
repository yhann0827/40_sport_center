# Connecting an HTML page to the API

## Prerequisites

Make sure your HTML form has an `id` attribute. That's how you can handle multiple forms in a page.

> Example:
```
    <form id="frmLoginSubmit">
```

Also, make sure each form input has an `id`.
> Example:
```
            <form id="frmLoginSubmit">
              <div class="details__text">
                <p>Email*</p>
                <input
                  type="text"
                  id="login_username"
                  name="username"
                  placeholder="Enter Your Email"
                  class="details__input"
                  required
                />
              </div>

              <div class="details__text">
                <p>Password*</p>
                <input
                  type="password"
                  id="login_password"
                  name="password"
                  placeholder="Enter Your Password"
                  class="details__input"
                  required
                />
              </div>

```

In the above code please note that both the `input` tags have the `required` attribute. With HTML5 adding `required` allows the browser to validate.

### Adding `jQuery`.

You can add `jQuery` using the _CDN_ version;

```
    <script src="https://code.jquery.com/jquery-3.6.3.min.js" integrity="sha256-pvPw+upLPUjgMXY0G+8O0xUf+/Im1MZjXxxgOcBQBXU=" crossorigin="anonymous"></script>
```

Next add a `<scrpt>` tag, before the end of the `</body>` tag.

```
    <script>
    // Functions or global variables here
    /* Function to return login form data as an object. */

    </script>
  </body>
</html>
```

You would need a javascript function to convert form data into an object. See examples below.

> This converts login form data into an object. Make sure to set the property names same as the database columns.
```
      var login_data = function() {
          return {
              username: $('#login_username').val(),
              password: $('#login_password').val()
          }
      };
```

> Similarly, below code is for the signup form.
```
      var signup_data = function() {
          return {
              first_name: $('#first_name').val(),
              last_name: $('#last_name').val(),
              username: $('#username').val(),
              password: $('#password').val(),
              email: $('#email').val(),
              address: $('#address').val(),
              date_of_birth: new Date($('#date_of_birth').val()),
              user_type: $('#user_type').val()
          }
      };
```

Finally, we need to add a function for posting the form to the API.
> Login form function.
```
      $('document').ready(function() {
          $('#frmLoginSubmit').submit(function(e) {
              e.preventDefault();
              $.ajax({
                  url: '/users/login',
                  type: 'POST',
                  data: JSON.stringify(login_data()),
                  dataType: 'json',
                  contentType: "application/json",
                  success: function () {
                      console.log('Logged in successfully');
                      window.location.href = "http://127.0.01:5000/";
                   },
                  error: function (e) { 
                      console.log("Error - submitting form", e);
                      //$('#messages').append('An error occurred');
                    }
              });
          });
      });
```

> In the above code `url` needs to be the bank-end API that handles the HTTP request.

> `data` must have the function call to the function that converts form data into an object e.g. _JSON.stringify(**login_data()**)_.

> `success` function tells the script what to do if the form submission was successful. e.g. _window.location.href = "http://127.0.01:5000/"_ means redirect to the home page.

> `error` function tells the script what to do if an error occurred e.g. _console.log("Error - submitting form", e);_ dumps the error returned into the dev tools console and _$('#messages').append('An error occurred');_ appends a message for the user in the `div` or `p` tags with an `id=message`.
