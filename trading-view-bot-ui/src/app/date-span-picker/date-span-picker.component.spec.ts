import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DateSpanPickerComponent } from './date-span-picker.component';

describe('DateSpanPickerComponent', () => {
  let component: DateSpanPickerComponent;
  let fixture: ComponentFixture<DateSpanPickerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DateSpanPickerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DateSpanPickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
