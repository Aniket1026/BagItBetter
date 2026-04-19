"use client";

import { useState } from "react";
import { PlusCircle, Trash2, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

export default function ProductComparison() {
  const [urls, setUrls] = useState([""]);
  const { toast } = useToast();

  const addUrlField = () => {
    setUrls([...urls, ""]);
  };

  const removeUrlField = (index: number) => {
    const newUrls = urls.filter((_, i) => i !== index);
    setUrls(newUrls);
  };

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const handleSubmit = () => {
    const nonEmptyUrls = urls.filter((url) => url.trim() !== "");
    if (nonEmptyUrls.length < 2) {
      toast({
        title: "Not enough URLs",
        description: "Please enter at least two valid product URLs to compare.",
        variant: "destructive",
      });
      return;
    }
    // Here you would typically send the URLs to your backend for processing
    console.log("Submitting URLs:", nonEmptyUrls);
    toast({
      title: "URLs submitted",
      description: `Processing ${nonEmptyUrls.length} product URLs for comparison.`,
    });
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>Product Comparison Tool</CardTitle>
          <CardDescription>
            Enter product URLs from e-commerce websites to compare and get
            recommendations.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {urls.map((url, index) => (
              <div key={index} className="flex items-center space-x-2">
                <Input
                  type="url"
                  placeholder="Enter product URL"
                  value={url}
                  onChange={(e) => handleUrlChange(index, e.target.value)}
                  className="flex-grow"
                />
                {urls.length > 1 && (
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => removeUrlField(index)}
                    className="flex-shrink-0"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))}
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" onClick={addUrlField}>
            <PlusCircle className="mr-2 h-4 w-4" /> Add URL
          </Button>
          <Button onClick={handleSubmit}>
            Compare Products <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}