import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddTickerFormComponent } from './add-ticker-form.component';

describe('AddTickerFormComponent', () => {
  let component: AddTickerFormComponent;
  let fixture: ComponentFixture<AddTickerFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddTickerFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddTickerFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
