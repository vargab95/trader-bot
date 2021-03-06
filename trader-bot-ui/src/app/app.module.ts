import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";

import "hammerjs";
import "chartjs-plugin-zoom";

import { ChartsModule } from "ng2-charts";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatCheckboxModule } from "@angular/material/checkbox";
import { MatDatepickerModule } from "@angular/material/datepicker";
import { MatNativeDateModule } from "@angular/material/core";
import { MatInputModule } from "@angular/material/input";
import { MatRadioModule } from "@angular/material/radio";
import { MatSelectModule } from "@angular/material/select";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import {
  NgxMatDatetimePickerModule,
  NgxMatTimepickerModule,
  NgxMatNativeDateModule,
} from "@angular-material-components/datetime-picker";
import { NgxMatMomentModule } from "@angular-material-components/moment-adapter";
import { ChartComponent } from "./chart/chart/chart.component";
import { DateSpanPickerComponent } from "./signals/date-span-picker/date-span-picker.component";
import { AddSignalFormComponent } from "./signals/add-signal-form/add-signal-form.component";
import { GraphComponent } from "./graph/graph.component";
import { LoginComponent } from "./auth/login/login.component";
import { SignupComponent } from "./auth/signup/signup.component";
import { MatFormFieldModule } from "@angular/material/form-field";
import { CookieService } from "ngx-cookie-service";
import { AuthenticationInterceptor } from "./auth/authentication.interceptor";
import { CommonModule } from "@angular/common";
import { NavbarComponent } from "./navbar/navbar.component";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { ComplexFilterComponent } from "./filtering/complex-filter/complex-filter.component";
import { FilterFormComponent } from "./filtering/filter-form/filter-form.component";

import { MatTableModule } from "@angular/material/table";
import { SignalListComponent } from "./signals/signal-list/signal-list.component";
import { MatDividerModule } from "@angular/material/divider";

import { MatDialogModule } from "@angular/material/dialog";

@NgModule({
  declarations: [
    AppComponent,
    ChartComponent,
    DateSpanPickerComponent,
    AddSignalFormComponent,
    GraphComponent,
    LoginComponent,
    SignupComponent,
    NavbarComponent,
    ComplexFilterComponent,
    FilterFormComponent,
    SignalListComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    ChartsModule,
    HttpClientModule,
    NgxMatDatetimePickerModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatInputModule,
    NgxMatDatetimePickerModule,
    NgxMatTimepickerModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    NgxMatMomentModule,
    MatRadioModule,
    MatSelectModule,
    MatCheckboxModule,
    MatNativeDateModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatToolbarModule,
    MatIconModule,
    MatTableModule,
    MatDividerModule,
    MatDialogModule,
  ],
  providers: [
    CookieService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthenticationInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
