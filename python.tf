resource "null_resource" "python_randomname" {
  triggers = {
    build_number = timestamp()
  }

  provisioner "local-exec" {
    command = "pip install --target ${path.module}/demobuilder/ --upgrade randomname"
  }
}

resource "null_resource" "python_requests" {
  triggers = {
    build_number = timestamp()
  }

  provisioner "local-exec" {
    command = "pip install --target ${path.module}/demobuilder/ --upgrade requests"
  }
}

resource "null_resource" "python_pytz" {
  triggers = {
    build_number = timestamp()
  }

  provisioner "local-exec" {
    command = "pip install --target ${path.module}/demobuilder/ --upgrade pytz"
  }
}
