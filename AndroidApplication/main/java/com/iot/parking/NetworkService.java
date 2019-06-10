package com.iot.parking;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;


public interface NetworkService {

    @GET("/getFlag")
    Call<Bon> get_flag();
    @GET("/sendLine/{ln}/")
    Call<Linenum> set_linenum(@Path("ln") int ln);
}
