package com.iot.parking;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    private NetworkService networkService;

    private Switch Switch1;
    private Switch Switch2;
    private Switch Switch3;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ApplicationController application = ApplicationController.getInstance();
        application.buildNetworkService("119.77.100.41", 8000);
        networkService = ApplicationController.getInstance().getNetworkService();
        Button button1 = (Button) findViewById(R.id.bt1);

        button1.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {

                // TODO : click event
                //GET+
                Call<Bon> versionCall = networkService.get_flag();
                versionCall.enqueue(new Callback<Bon>() {
                    @Override
                    public void onResponse(Call<Bon> call, Response<Bon> response) {
                        if(response.isSuccessful()) {
                            Bon bon = response.body();
                            TextView text1 = (TextView) findViewById(R.id.tv1) ;
                            String version_txt = "";

                            int bon_flag = bon.getFlag();

                            text1.setText( Integer.toString(bon_flag));
                        } else {
                            int StatusCode = response.code();
                            Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                        }
                    }

                    @Override
                    public void onFailure(Call<Bon> call, Throwable t) {
                        Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                    }
                });
            }
        });

        this.Switch1 = (Switch) findViewById(R.id.switch1);
        this.Switch2 = (Switch) findViewById(R.id.switch2);
        this.Switch3 = (Switch) findViewById(R.id.switch3);

        this.Switch1.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked == true){

                    Call<Linenum> versionCall = networkService.set_linenum(210);
                    versionCall.enqueue(new Callback<Linenum>() {
                        @Override
                        public void onResponse(Call<Linenum> call, Response<Linenum> response) {
                            if(response.isSuccessful()) {
                                Linenum bon = response.body();

                            } else {
                                int StatusCode = response.code();
                                Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                            }
                        }

                        @Override
                        public void onFailure(Call<Linenum> call, Throwable t) {
                            Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                        }
                    });

                    Toast.makeText(MainActivity.this, "1번 라인 등록", Toast.LENGTH_SHORT).show();


                } else {

                    Call<Linenum> versionCall = networkService.set_linenum(210);
                    versionCall.enqueue(new Callback<Linenum>() {
                        @Override
                        public void onResponse(Call<Linenum> call, Response<Linenum> response) {
                            if(response.isSuccessful()) {
                                Linenum bon = response.body();

                            } else {
                                int StatusCode = response.code();
                                Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                            }
                        }

                        @Override
                        public void onFailure(Call<Linenum> call, Throwable t) {
                            Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                        }
                    });
                    Toast.makeText(MainActivity.this, "1번 라인 해제", Toast.LENGTH_SHORT).show();

                }
            }
        });




        this.Switch2.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked == true){

                    Call<Linenum> versionCall = networkService.set_linenum(160);
                    versionCall.enqueue(new Callback<Linenum>() {
                        @Override
                        public void onResponse(Call<Linenum> call, Response<Linenum> response) {
                            if(response.isSuccessful()) {
                                Linenum bon = response.body();

                            } else {
                                int StatusCode = response.code();
                                Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                            }
                        }

                        @Override
                        public void onFailure(Call<Linenum> call, Throwable t) {
                            Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                        }
                    });

                    Toast.makeText(MainActivity.this, "2번 라인 등록", Toast.LENGTH_SHORT).show();


                } else {

                    Call<Linenum> versionCall = networkService.set_linenum(160);
                    versionCall.enqueue(new Callback<Linenum>() {
                        @Override
                        public void onResponse(Call<Linenum> call, Response<Linenum> response) {
                            if(response.isSuccessful()) {
                                Linenum bon = response.body();

                            } else {
                                int StatusCode = response.code();
                                Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                            }
                        }

                        @Override
                        public void onFailure(Call<Linenum> call, Throwable t) {
                            Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                        }
                    });
                    Toast.makeText(MainActivity.this, "2번 라인 해제", Toast.LENGTH_SHORT).show();

                }
            }
        });




        this.Switch3.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked == true){

                    Call<Linenum> versionCall = networkService.set_linenum(110);
                    versionCall.enqueue(new Callback<Linenum>() {
                        @Override
                        public void onResponse(Call<Linenum> call, Response<Linenum> response) {
                            if(response.isSuccessful()) {
                                Linenum bon = response.body();

                            } else {
                                int StatusCode = response.code();
                                Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                            }
                        }

                        @Override
                        public void onFailure(Call<Linenum> call, Throwable t) {
                            Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                        }
                    });

                    Toast.makeText(MainActivity.this, "3번 라인 등록", Toast.LENGTH_SHORT).show();


                } else {

                    Call<Linenum> versionCall = networkService.set_linenum(110);
                    versionCall.enqueue(new Callback<Linenum>() {
                        @Override
                        public void onResponse(Call<Linenum> call, Response<Linenum> response) {
                            if(response.isSuccessful()) {
                                Linenum bon = response.body();

                            } else {
                                int StatusCode = response.code();
                                Log.i(ApplicationController.TAG, "Status Code : " + StatusCode);
                            }
                        }

                        @Override
                        public void onFailure(Call<Linenum> call, Throwable t) {
                            Log.i(ApplicationController.TAG, "Fail Message : " + t.getMessage());
                        }
                    });
                    Toast.makeText(MainActivity.this, "3번 라인 해제", Toast.LENGTH_SHORT).show();

                }
            }
        });


    }
}



