import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { AuthenticationService } from '../authentication.service';
import { Account } from '../account.entity';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  signupForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthenticationService,
    private router: Router
  ) {}

  ngOnInit() {
    this.signupForm = this.formBuilder.group({
      email: '',
      password: ''
    });
  }

  signUp() {
    const account = new Account();

    account.email = this.signupForm.value.email;
    account.password = this.signupForm.value.password;

    this.authService.signUp(account).subscribe(
      response => {
        this.router.navigate(['auth', 'login']);
      },
      error => {
        console.log(error);
      }
    );
  }
}
