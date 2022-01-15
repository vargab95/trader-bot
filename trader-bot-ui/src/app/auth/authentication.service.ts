import { Injectable, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Account } from './account.entity';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  currentAccount: Account = null;

  constructor(private cookieService: CookieService, private http: HttpClient) {
    if (this.cookieService.check('token')) {
      this.currentAccount = new Account();
      this.currentAccount.token = this.cookieService.get('token');
    }
  }

  logIn(logInInfo: Account): Observable<Account> {
    this.currentAccount = logInInfo;
    return this.http
      .post<Account>(environment.apiBaseUrl + 'auth/login', {
        email: logInInfo.email,
        password: logInInfo.password
      })
      .pipe<Account>(
        map(response => {
          this.currentAccount.token = response.token;
          this.cookieService.set('token', response.token);
          return this.currentAccount;
        })
      );
  }

  logOut() {
    this.currentAccount = null;
    this.cookieService.delete('token');
  }

  signUp(userInfo: Account) {
    this.currentAccount = userInfo;
    return this.http.post(environment.apiBaseUrl + 'auth/signup', {
      email: userInfo.email,
      password: userInfo.password
    });
  }

  getCurrentAccount(): Account {
    return this.currentAccount;
  }

  isAuthenticated(): boolean {
    return this.currentAccount !== null && !!this.currentAccount.token;
  }
}
