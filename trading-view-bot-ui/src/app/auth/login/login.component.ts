import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { AuthenticationService } from '../authentication.service';
import { Account } from '../account.entity';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthenticationService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      email: '',
      password: ''
    });
  }

  logIn() {
    const account = new Account();

    account.email = this.loginForm.value.email;
    account.password = this.loginForm.value.password;

    this.authService.logIn(account).subscribe(
      response => {
        this.router.navigate(['graph']);
      },
      error => {
        console.log(error);
      }
    );
  }

  onSignup() {
    this.router.navigate(['auth', 'signup']);
  }
}
