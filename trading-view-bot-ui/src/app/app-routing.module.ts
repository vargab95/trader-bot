import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './auth/login/login.component';
import { SignupComponent } from './auth/signup/signup.component';
import { GraphComponent } from './graph/graph.component';
import { AuthenticationGuardService } from './auth/authentication.guard';

const routes: Routes = [
  { path: 'auth/login', component: LoginComponent },
  { path: 'auth/signup', component: SignupComponent },
  {
    path: '',
    redirectTo: 'graph',
    pathMatch: 'full'
  },
  {
    path: 'graph',
    component: GraphComponent,
    canActivate: [AuthenticationGuardService]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
